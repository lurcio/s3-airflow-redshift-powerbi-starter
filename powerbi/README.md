
# Power BI Semantic Model (PBIP) — Placeholder

Create a **PBIP project** here named `SalesModel.pbip` that connects to Redshift (curated schema) and defines at least 3 measures:

```DAX
Total Sales = SUM('fact_sales'[amount])
Avg Order Value = DIVIDE([Total Sales], DISTINCTCOUNT('fact_sales'[order_id]))
Orders YoY =
VAR CurrentYear = YEAR(MAX('fact_sales'[order_date]))
VAR LastYear = CurrentYear - 1
VAR OrdersCurrent = COUNTROWS(FILTER('fact_sales', YEAR('fact_sales'[order_date]) = CurrentYear))
VAR OrdersLast    = COUNTROWS(FILTER('fact_sales', YEAR('fact_sales'[order_date]) = LastYear))
RETURN DIVIDE(OrdersCurrent - OrdersLast, OrdersLast)
```

> Document connection method (DirectQuery or Import), credentials handling, and any performance considerations.
