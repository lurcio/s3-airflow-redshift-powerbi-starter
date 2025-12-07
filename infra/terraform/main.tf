
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "random_id" "suffix" { byte_length = 4 }

resource "aws_s3_bucket" "raw" {
  bucket = "${var.project}-raw-${random_id.suffix.hex}"
}

# IAM role for Redshift to read from S3
resource "aws_iam_role" "redshift_load" {
  name               = "${var.project}-redshift-load"
  assume_role_policy = data.aws_iam_policy_document.redshift_trust.json
}

data "aws_iam_policy_document" "redshift_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["redshift.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "s3_access" {
  role   = aws_iam_role.redshift_load.id
  policy = data.aws_iam_policy_document.s3_policy.json
}

data "aws_iam_policy_document" "s3_policy" {
  statement {
    actions   = ["s3:GetObject", "s3:ListBucket"]
    resources = [aws_s3_bucket.raw.arn, "${aws_s3_bucket.raw.arn}/*"]
  }
}

# Redshift Serverless
resource "aws_redshiftserverless_namespace" "ns" {
  namespace_name = "${var.project}-ns"
  db_name        = "analytics"
}

resource "aws_redshiftserverless_workgroup" "wg" {
  workgroup_name = "${var.project}-wg"
  namespace_name = aws_redshiftserverless_namespace.ns.namespace_name
  base_capacity  = 8
}
