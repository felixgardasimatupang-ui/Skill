---
name: ask-telemetry-instrumentor
description: Otomatisasi injeksi kode instrumentasi untuk pelacakan performa dan error (OpenTelemetry, Sentry, atau Prometheus).
triggers: ["opentelemetry", "sentry", "instrumentation", "error tracking", "distributed tracing", "apm"]
---

# Telemetry Instrumentor

Menginstrumen kode dengan telemetry, distributed tracing, dan error tracking secara otomatis.

<critical_constraints>
- ❌ NO menyentuh handler error tanpa menambah telemetry
- ❌ NO mengekspos trace ID ke user tanpa sanitasi
- ✅ WAJIB inject OpenTelemetry SDK di entry point aplikasi
- ✅ WAJIB propagasi trace context lintas service (W3C Trace Context)
- ✅ WAJIB capture unhandled exceptions dan promise rejections
- ✅ WAJIB set proper span attributes (HTTP method, URL, status code)
</critical_constraints>

<heuristics>
- Express/Koa → otel/auto-instrumentations-node (http, express)
- Next.js → @sentry/nextjs + otel/auto-instrumentations-web
- Prisma → @prisma/instrumentation untuk query tracing
- Background jobs (Bull, Sidekiq) → wrap handler dengan span
- Database query lambat → custom span dengan DB statement
- Custom business logic → tambah span manual untuk critical path
</heuristics>

## Purpose

Memastikan semua komponen aplikasi terinstrumentasi dengan baik sehingga tim dapat mendeteksi, mendiagnosis, dan merespons error dengan cepat.

## Usage

Gunakan ketika:
- Setup awal proyek baru (instrumentasi sejak hari pertama)
- Menambah service / microservice baru
- Debugging issue yang sulit direproduksi
- Performa menurun — perlu tracing end-to-end
- Integrasi dengan APM (Datadog, New Relic, Grafana Tempo)

### Core Protocol

1. **Init SDK**: Setup OpenTelemetry SDK + exporter (Jaeger, Tempo, console)
2. **Auto-instrumentation**: Pasang package auto-instrumentasi sesuai framework
3. **Manual Spans**: Tambah span untuk business logic critical
4. **Error Capture**: Integrasi Sentry untuk error tracking + breadcrumbs
5. **Context Propagation**: Propagasi trace context via HTTP headers

## Examples

### OpenTelemetry Init (Node.js)
```ts
import { NodeSDK } from '@opentelemetry/sdk-node'
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({ url: process.env.OTEL_EXPORTER_URL }),
  instrumentations: [getNodeAutoInstrumentations()],
})

sdk.start()
process.on('SIGTERM', () => sdk.shutdown())
```

### Manual Span for Business Logic
```ts
import { trace } from '@opentelemetry/api'

const tracer = trace.getTracer('payment-service')

async function processPayment(orderId: string) {
  const span = tracer.startSpan('processPayment', { attributes: { orderId } })
  try {
    const result = await paymentGateway.charge(orderId)
    span.setAttribute('payment.status', result.status)
    span.setStatus({ code: SpanStatusCode.OK })
    return result
  } catch (err) {
    span.recordException(err)
    span.setStatus({ code: SpanStatusCode.ERROR })
    throw err
  } finally {
    span.end()
  }
}
```

### Sentry Integration
```ts
import * as Sentry from '@sentry/node'
import { nodeProfilingIntegration } from '@sentry/profiling-node'

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  integrations: [nodeProfilingIntegration()],
  tracesSampleRate: 1.0,
  profilesSampleRate: 0.5,
})
```

## Best Practices

- **Sampling**: 100% di dev/staging, 0.1-1% di production (sesuai volume)
- **Span Attributes**: Minimal — jangan log PII atau sensitive data
- **Breadcrumbs**: Tambah breadcrumbs untuk user actions (Sentry)
- **Alerting**: Setup alert untuk error rate spike + latency p95 > 1s
- **Dashboard**: Grafana / Datadog dashboard untuk trace metrics
