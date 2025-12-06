
-- Example quality checks the candidate can expand:
-- 1) No NULLs in primary fields
SELECT COUNT(*) AS null_orders FROM curated.fact_sales WHERE order_id IS NULL;
-- 2) Amount non-negative
SELECT COUNT(*) AS bad_amount FROM curated.fact_sales WHERE amount < 0;
-- 3) Row count threshold
SELECT COUNT(*) AS rowcount FROM curated.fact_sales;
