---
name: ask-log-analyzer
description: Menganalisis log server, mendeteksi pola anomali, dan melacak pergerakan request menggunakan trace ID dari frontend hingga backend.
triggers: ["log analysis", "error pattern", "trace id", "anomaly detection", "debug production", "server log"]
---

# Log Analyzer

Menganalisis log server untuk mendeteksi anomali, pola error berulang, dan melacak request dari frontend ke backend.

<critical_constraints>
- ❌ NO membaca log line by line untuk volume besar — gunakan tools (grep, jq, awk)
- ❌ NO mengambil kesimpulan dari 1 error — cari pattern
- ✅ WAJIB cari trace ID untuk menghubungkan request frontend → backend → database
- ✅ WAJIB kategorikan error: 4xx (client) vs 5xx (server) vs timeout
- ✅ WAJIB cek timestamp untuk melihat timeline kejadian
- ✅ WAJIB korelasikan dengan deployment timeline (apakah error mulai setelah deploy?)
</critical_constraints>

<heuristics>
- Error spike setelah deploy → rollback atau hotfix
- 5xx error pada endpoint yang sama → cek database / upstream dependency
- Timeout konsisten setiap jam → cron job / worker overload
- Error hanya dari 1 user → cek data spesifik user tersebut
- Client IP tertentu menghasilkan banyak 4xx → rate limit atau block
- Memory leak pattern → GC overhead limit exceeded, heap growing
</heuristics>

## Purpose

Mempercepat diagnosis masalah production dengan menganalisis log secara sistematis, menghubungkan trace antar service, dan mengidentifikasi root cause.

## Usage

Gunakan ketika:
- Ada insiden production (error spike, downtime)
- Debugging issue yang sulit direproduksi
- Performance regression
- Keamanan (brute force, scraping detection)
- Audit / post-mortem

### Core Protocol

1. **Time Window**: Tentukan kapan error mulai (sebelum/sesudah deploy?)
2. **Filter by Severity**: ERROR, WARN, FATAL
3. **Group by Endpoint**: Endpoint mana yang paling banyak error?
4. **Trace Request**: Ikuti trace ID dari ingress → service → DB
5. **Correlate**: Hubungkan dengan metrics (CPU, memory, DB connections)
6. **Identify Pattern**: Apakah error berkala? Terkait data tertentu? Hanya user tertentu?

## Examples

### Cari trace ID dari frontend ke backend
```bash
grep "trace-id" frontend.log | tail -5
grep "trace_id=abc123" backend-*.log
grep "abc123" postgresql.log
```

### Deteksi anomali dengan grep patterns
```bash
grep -oP '"method":"\w+","path":"/[^"]+"' app.log | sort | uniq -c | sort -rn
grep "duration.*>.*1000" sql.log
grep -oP '"ip":"[^"]+"' access.log | sort | uniq -c | sort -rn | head -10
```

### Structured Log Query (JSON logs → jq)
```bash
jq 'select(.level=="ERROR" and .timestamp > (now - 3600))' logs.json
jq 'select(.level=="ERROR") | .service' logs.json | sort | uniq -c | sort -rn
```

## Best Practices

- **Structured Logging**: JSON format — memudahkan query dengan jq
- **Trace ID**: Propagasi dari frontend → semua backend → database
- **Log Levels**: ERROR (actionable), WARN (attention), INFO (audit), DEBUG (dev only)
- **Retention**: Hot storage (7 hari), Cold storage (90 hari), Archive (1 tahun)
- **Alerting**: Setup alert untuk error rate > 1% per endpoint
- **Dashboard**: Grafana Loki / ELK Stack untuk visualisasi
