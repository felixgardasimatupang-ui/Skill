# Full Table Scan Test

## Input
```sql
SELECT * FROM orders WHERE status = 'pending' ORDER BY total DESC;
```
EXPLAIN output: `Seq Scan on orders (cost=0.00..5000.00 rows=25000)`

## Expected Output
"Missing index on `status` + `total` columns. Create composite index: `CREATE INDEX idx_orders_status_total ON orders (status, total DESC)`."
