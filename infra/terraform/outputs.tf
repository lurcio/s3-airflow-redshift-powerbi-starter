
output "s3_bucket_name" { value = aws_s3_bucket.raw.bucket }
output "redshift_workgroup_name" { value = aws_redshiftserverless_workgroup.wg.workgroup_name }
output "iam_role_arn" { value = aws_iam_role.redshift_load.arn }
