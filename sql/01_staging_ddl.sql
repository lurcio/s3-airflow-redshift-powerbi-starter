
CREATE TABLE IF NOT EXISTS staging.staging_sales_orders(
  order_id BIGINT,
  customer_id BIGINT,
  order_date DATE,
  amount NUMERIC(18,2)
);
