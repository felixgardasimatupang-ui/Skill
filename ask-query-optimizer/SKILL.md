---
name: ask-query-optimizer
description: Menganalisis bottleneck performa, indeks database, dan optimasi query (ORM/SQL).
triggers: ["slow query", "database bottleneck", "optimize query", "n+1 problem", "index tuning", "query performance"]
---

# Query Optimizer

Menganalisis bottleneck performa database, merancang indeks, dan mengoptimasi query SQL maupun ORM.

<critical_constraints>
- ❌ NO mengubah query tanpa explain plan terlebih dahulu
- ❌ NO menambah indeks tanpa menganalisis selectivity dan write overhead
- ❌ NO menggunakan SELECT * di production
- ❌ NO N+1 query di ORM — wajib eager loading
- ✅ WAJIB membaca EXPLAIN ANALYZE sebelum optimasi
- ✅ WAJIB mengukur before/after performance
- ✅ WAJIB mempertimbangkan composite index untuk multi-filter query
</critical_constraints>

<heuristics>
- Query lambat dengan full table scan → cek WHERE clause, tambah index
- N+1 di ORM (Entity Framework, Prisma, Sequelize, Django ORM) → ganti dengan JOIN / include / select_related
- Pagination dengan OFFSET besar → ganti ke keyset pagination (cursor-based)
- ORDER BY tanpa index → tambah covering index
- Subquery di WHERE IN → ganti ke JOIN atau EXISTS
- UPDATE dengan JOIN complex → batch processing
</heuristics>

## Purpose

Skill ini memastikan akses data efisien dengan menganalisis bottleneck, menerapkan indexing strategy, dan mengoptimasi query SQL/ORM tanpa mengubah perilaku bisnis.

## Usage

Gunakan ketika:
- Ada laporan "halaman lambat" atau "API timeout"
- Query dieksekusi > 500ms di production
- Menemukan N+1 query saat code review
- Mendesain schema untuk fitur baru dengan volume data besar
- Melakukan migration dengan downtime minimal

### Core Protocol

1. **Capture Query**: Dapatkan query lambat dari logs, slow query log, atau APM (Datadog, New Relic, Sentry).
2. **EXPLAIN**: Jalankan `EXPLAIN (ANALYZE, BUFFERS)` — identifikasi seq scan, nested loop, sort.
3. **Diagnose Root Cause**:
   - Missing index → `CREATE INDEX CONCURRENTLY`
   - Subquery tidak efisien → rewrite ke JOIN/CTE
   - ORM lazy loading → eager loading
4. **Apply Fix**: Implementasi perubahan dengan safety (migration, index tanpa locking).
5. **Verify**: Re-run EXPLAIN + ukur response time.

## Examples

### Sebelum — N+1 via ORM (Prisma)
```ts
const users = await prisma.user.findMany()
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { userId: user.id } })
}
// 1 query user + N query post = 1+N round trips
```

### Sesudah — Eager loading
```ts
const users = await prisma.user.findMany({
  include: { posts: true }
})
// 1 query with LEFT JOIN
```

### Sebelum — Full table scan
```sql
SELECT * FROM transactions WHERE created_at > '2025-01-01' ORDER BY amount DESC;
-- Seq Scan on transactions (cost=0.00..10000.00)
```

### Sesudah — Composite index
```sql
CREATE INDEX CONCURRENTLY idx_transactions_date_amount
ON transactions (created_at, amount DESC);

EXPLAIN ANALYZE
SELECT id, amount FROM transactions WHERE created_at > '2025-01-01' ORDER BY amount DESC;
-- Index Only Scan (cost=0.00..500.00)
```

## Best Practices

- **Index**: 1 index per query pattern; hindari over-indexing (> 5 indeks per tabel)
- **Partial Index**: Untuk data dengan filter boolean/satus
- **Covering Index**: Include columns untuk index-only scan
- **Batch Processing**: Untuk UPDATE/DELETE jutaan baris, proses per 1000 baris
- **Read Replica**: Arahkan query heavy/batch ke read replica
- **Connection Pool**: Atur pool size (CPU core * 2 + 1)
