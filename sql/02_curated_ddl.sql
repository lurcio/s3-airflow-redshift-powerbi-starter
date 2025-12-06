
CREATE TABLE IF NOT EXISTS curated.fact_sales AS
SELECT
  order_id,
  customer_id,
  order_date,
  DATE_TRUNC('month', order_date) AS order_month,
  amount
FROM staging.staging_sales_orders;
