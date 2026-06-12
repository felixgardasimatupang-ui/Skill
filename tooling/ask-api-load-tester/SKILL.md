---
name: ask-api-load-tester
description: Menguji ketahanan beban API (K6/Artillery) sebelum rilis ke tahap production.
triggers: ["load test", "k6", "artillery", "stress test", "performance test", "benchmark", "api load"]
---

# API Load Tester

Merancang dan menjalankan load test untuk mengukur performa API di bawah tekanan.

<critical_constraints>
- ❌ NO load test di production langsung — gunakan staging dulu
- ❌ NO hanya 1 skenario — variasikan endpoint, payload, dan pola beban
- ✅ WAJIB tentukan SLO sebelum test: latency p95 < 500ms, error < 1%
- ✅ WAJIB warm-up phase sebelum measurement
- ✅ WAJIB monitor resource (CPU, memory, DB connections) selama test
- ✅ WAJIB ramp-up gradual — jangan spike langsung ke peak
</critical_constraints>

<heuristics>
- Smoke test → 1 VU untuk verifikasi fungsional
- Load test → target throughput normal (50-100 VU)
- Stress test → naikkan hingga 2-5x target (cari breaking point)
- Soak test → beban sustain 1-2 jam (deteksi memory leak)
- Spike test → lonjakan tiba-tiba 10x dalam 10 detik
- Endpoint lambat → cek query DB, caching, atau external API call
</heuristics>

## Purpose

Memvalidasi bahwa API dapat menangani beban yang diharapkan dengan latency dan error rate dalam batas yang ditentukan.

## Usage

Gunakan ketika:
- Sebelum rilis major / public launch
- Setelah perubahan arsitektur (migration, scaling)
- Menentukan kapasitas server (autoscaling threshold)
- Debugging performance regression
- Validasi SLO/SLA

### Core Protocol

1. **Define SLO**: Target latency (p50, p95, p99), throughput (RPS), error rate
2. **Design Scenario**: Endpoints, payload, authentication, think time
3. **Setup Environment**: Staging / dedicated test environment
4. **Execute**: Ramp-up → steady → ramp-down
5. **Monitor**: Dashboard metrics (CPU, memory, connections)
6. **Report**: Latency distribution, error breakdown, bottleneck

## Examples

### K6 — Load Test Skenario
```js
import http from 'k6/http'
import { check, sleep } from 'k6'

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // ramp-up
    { duration: '5m', target: 50 },   // steady
    { duration: '1m', target: 0 },    // ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
  },
}

export default function () {
  const res = http.get('https://api.example.com/students', {
    headers: { Authorization: 'Bearer token' }
  })
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 300ms': (r) => r.timings.duration < 300,
  })
  sleep(1)
}
```

### Artillery — Mixed Workload
```yaml
config:
  target: "https://api.example.com"
  phases:
    - duration: 60
      arrivalRate: 10
      rampTo: 50
      name: "Warm up"
    - duration: 300
      arrivalRate: 50
      name: "Sustained load"
  defaults:
    headers:
      Authorization: "Bearer token"

scenarios:
  - flow:
    - get:
        url: "/students"
        capture:
          json: "$.data[0].id"
          as: "studentId"
    - get:
        url: "/students/{{ studentId }}"
    - post:
        url: "/students"
        json:
          name: "Test Student"
          email: "test{{ $randomString(5) }}@example.com"
```

## Best Practices

- **Test Data**: Gunakan data terisolasi — jangan campur dengan traffic nyata
- **Idempotency**: Pastikan endpoint aman dipanggil berulang
- **Cleanup**: Hapus test data setelah selesai
- **Network Conditions**: Simulasikan latency + bandwidth realistis
- **Reports**: Ekspor JSON / HTML report untuk analisis
- **CI Integration**: Jalankan smoke test di CI, full load test scheduled
