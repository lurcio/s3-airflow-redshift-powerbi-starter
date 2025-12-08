
# S3 → Airflow → Redshift → Power BI — Starter Template

This repo is a minimal, production-like template you can hand to a candidate to build an end‑to‑end pipeline:

- **Land** CSV data in **Amazon S3**
- **Orchestrate** an **Apache Airflow** DAG to load into **Amazon Redshift (Serverless)**
- **Model** a **Power BI semantic model** (.pbip) against curated tables
- **Validate** with lightweight data quality checks
- **Automate** lint/tests via **GitHub Actions**

> 🔧 The template is intentionally opinionated but lightweight. The candidate should flesh out details, implement incremental strategy, and document trade‑offs in their README.

## Repo layout
```
.
├─ infra/terraform/            # S3, IAM role, Redshift Serverless
├─ airflow/                    # Docker Compose + DAGs + tests
│  ├─ docker-compose.yaml
│  ├─ .env.sample
│  ├─ dags/
│  │  ├─ s3_to_redshift_pipeline.py
│  │  └─ README.md
│  ├─ tests/
│  │  └─ test_dag_structure.py
├─ sql/                        # Schemas, DDL, transformations
│  ├─ 00_schema.sql
│  ├─ 01_staging_ddl.sql
│  ├─ 02_curated_ddl.sql
│  └─ 03_quality.sql
├─ powerbi/                    # Placeholder PBIP project (to be created by candidate)
│  └─ README.md
├─ data/sample/                # Tiny sample file
│  └─ sales_orders.csv
├─ docs/                       # Diagrams and notes
│  └─ architecture.md
└─ .github/workflows/          # CI pipeline
   └─ ci.yml
```

## Quick start

### 1) Provision AWS infrastructure (Terraform)
```bash
cd infra/terraform
terraform init
terraform apply -var="project=pre-assessment" -var="region=eu-west-2" -auto-approve
```
Record outputs (S3 bucket, IAM role ARN, Redshift workgroup). The candidate should add more variables/outputs as needed.

### 2) Configure Airflow environment
Copy `airflow/.env.sample` to `airflow/.env` and fill values.

```bash
cd airflow
cp .env.sample .env
# edit .env with AWS keys/region, S3 bucket, Redshift database/workgroup/role ARN
```

### 3) Start Airflow and run the DAG
```bash
docker compose -f airflow/docker-compose.yaml up -d
# Open http://localhost:8080 (user: admin / pass: admin)
```
Set Airflow Variables (UI) if you prefer templating instead of env‑based configuration. Trigger `s3_to_redshift_pipeline`.

### 4) Upload sample data to S3
```bash
aws s3 cp data/sample/sales_orders.csv s3://<your-bucket>/raw/sales_orders/sales_orders_test.csv
```

### 5) Open or create the Power BI semantic model
Read `powerbi/README.md` for guidance to create a PBIP project that connects to Redshift curated tables.

## CI
On every push/PR, **GitHub Actions** runs Python lint + DAG import + unit tests.

## What the candidate should deliver
- Working infra (AWS S3, IAM, Redshift Serverless) — preferably via Terraform
- Airflow DAG that loads staging → curated with basic data quality checks
- Power BI PBIP project with at least 3 measures and a small report
- README with architecture, setup, run, validation, troubleshooting
- Evidence (screenshots, logs) in `docs/`

## Cleanup
```bash
cd infra/terraform
terraform destroy -auto-approve
```

---

### Architecture (ASCII)
```
[GitHub Actions CI] --lint/tests--> [Repo]
               +--(optional terraform apply)--> [AWS: S3, IAM, Redshift Serverless]

[S3: sales_orders.csv] --(Airflow COPY)--> [Redshift: staging.sales_orders]
                     --SQL transform-->    [curated.fact_sales]

[Power BI (.pbip)] --DirectQuery/Import--> [Redshift curated]
```
