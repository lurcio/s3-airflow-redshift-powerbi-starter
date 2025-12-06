
# Airflow DAGs

This folder contains the S3 → Redshift pipeline DAG. Configure via environment variables or Airflow Variables.

Required parameters:
- `S3_BUCKET`
- `REDSHIFT_SERVERLESS_WORKGROUP`
- `REDSHIFT_DATABASE`
- `REDSHIFT_IAM_ROLE_ARN`

Optional: create Airflow Variables with the same names to use templating.
