from datetime import datetime
import os
from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator
from airflow.providers.amazon.aws.operators.redshift_data import (
    RedshiftDataOperator,
)

# Read from env; candidate may switch to Airflow Variables
S3_BUCKET = os.getenv("S3_BUCKET")
IAM_ROLE_ARN = os.getenv("REDSHIFT_IAM_ROLE_ARN")
REDSHIFT_DB = os.getenv("REDSHIFT_DATABASE", "analytics")
REDSHIFT_WORKGROUP = os.getenv("REDSHIFT_SERVERLESS_WORKGROUP")

STAGING_TABLE = "staging_sales_orders"
CURATED_TABLE = "fact_sales"
S3_PREFIX = "raw/sales_orders/"

with DAG(
    dag_id="s3_to_redshift_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["s3", "redshift", "powerbi"],
) as dag:

    start = EmptyOperator(task_id="start")

    create_schemas = RedshiftDataOperator(
        task_id="create_schemas",
        database=REDSHIFT_DB,
        workgroup_name=REDSHIFT_WORKGROUP,
        sql="""
        CREATE SCHEMA IF NOT EXISTS staging;
        CREATE SCHEMA IF NOT EXISTS curated;
        """,
    )

    create_staging = RedshiftDataOperator(
        task_id="create_staging",
        database=REDSHIFT_DB,
        workgroup_name=REDSHIFT_WORKGROUP,
        sql=f"""
        CREATE TABLE IF NOT EXISTS staging.{STAGING_TABLE}(
          order_id BIGINT,
          customer_id BIGINT,
          order_date DATE,
          amount NUMERIC(18,2)
        );
        TRUNCATE TABLE staging.{STAGING_TABLE};
        """,
    )

    copy_from_s3 = RedshiftDataOperator(
        task_id="copy_from_s3",
        database=REDSHIFT_DB,
        workgroup_name=REDSHIFT_WORKGROUP,
        sql=f"""
        COPY staging.{STAGING_TABLE}
        FROM 's3://{S3_BUCKET}/{S3_PREFIX}'
        IAM_ROLE '{IAM_ROLE_ARN}'
        FORMAT AS CSV IGNOREHEADER 1 TIMEFORMAT AS 'auto';
        """,
    )

    create_curated = RedshiftDataOperator(
        task_id="create_curated",
        database=REDSHIFT_DB,
        workgroup_name=REDSHIFT_WORKGROUP,
        sql=f"""
        CREATE TABLE IF NOT EXISTS curated.{CURATED_TABLE} AS
        SELECT
          order_id,
          customer_id,
          order_date,
          DATE_TRUNC('month', order_date) AS order_month,
          amount
        FROM staging.{STAGING_TABLE};
        """,
    )

    dq_rowcount = RedshiftDataOperator(
        task_id="dq_rowcount",
        database=REDSHIFT_DB,
        workgroup_name=REDSHIFT_WORKGROUP,
        sql=f"""
        -- Fail if zero rows
        DO $$
        DECLARE c INT;
        BEGIN
          SELECT COUNT(*) INTO c FROM curated.{CURATED_TABLE};
          IF c = 0 THEN
            RAISE EXCEPTION 'DQ failed: curated table is empty';
          END IF;
        END $$;
        """,
    )

    finish = EmptyOperator(task_id="finish")

    chain(
        start,
        create_schemas,
        create_staging,
        copy_from_s3,
        create_curated,
        dq_rowcount,
        finish,
    )
