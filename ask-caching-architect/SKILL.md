---
name: ask-caching-architect
description: Merancang strategi caching (Redis/Memcached) dan mitigasi cache invalidation.
triggers: ["cache strategy", "redis", "cache invalidation", "caching", "response time", "reduce latency"]
---

# Caching Architect

Merancang dan mengimplementasikan strategi caching yang tepat untuk mengurangi latency dan beban database.

<critical_constraints>
- ❌ NO cache-all — setiap data punya TTL dan strategi sendiri
- ❌ NO cache tanpa invalidation plan
- ❌ NO menyimpan PII di cache tanpa enkripsi
- ✅ WAJIB punya fallback ketika cache miss (Cache-Aside / Read-Through)
- ✅ WAJIB monitor cache hit ratio (> 80%)
- ✅ WAJIB set TTL yang realistis berdasarkan frekuensi perubahan data
</critical_constraints>

<heuristics>
- Data jarang berubah (konfigurasi, master data) → cache panjang (TTL 1-24 jam)
- Data sering berubah (stok, saldo) → cache pendek + write-through / write-behind
- Halaman publik (homepage, artikel) → full-page cache + CDN
- User session → Redis with TTL = session lifetime
- API rate limiting → sliding window di Redis
- Cache stampede → lock/mutex atau probabilistic early expiration
</heuristics>

## Purpose

Memastikan sistem tidak melakukan komputasi berulang atau query database berlebihan dengan menerapkan strategi caching yang tepat, aman, dan mudah dikelola.

## Usage

Gunakan ketika:
- Response time API > 200ms karena query berulang
- Database CPU > 70% akibat read-heavy workload
- Data yang sama diminta ribuan kali per detik
- Mendesain arsitektur untuk skala tinggi (1000+ RPS)
- Ingin mengurangi biaya database

### Core Protocol

1. **Identify Hot Data**: Analisis query mana yang paling sering dipanggil.
2. **Choose Strategy**: Pilih pattern caching (Cache-Aside, Read-Through, Write-Through, Write-Behind).
3. **Design TTL & Eviction**: LRU, LFU, atau TTL-based.
4. **Handle Invalidation**: Event-driven (pub/sub), webhook, atau time-based.
5. **Monitor**: Hit ratio, memory usage, eviction rate.

## Examples

### Cache-Aside (paling umum)
```ts
async function getUser(id: string) {
  const cacheKey = `user:${id}`
  let user = await redis.get(cacheKey)
  if (!user) {
    user = await db.user.findUnique({ where: { id } })
    await redis.setex(cacheKey, 300, JSON.stringify(user))
  }
  return user
}
```

### Write-Through + Cache Eviction
```ts
async function updateUser(id: string, data: any) {
  const user = await db.user.update({ where: { id }, data })
  await redis.setex(`user:${id}`, 300, JSON.stringify(user))
  await redis.del(`users:list`) // invalidate list cache
  return user
}
```

## Best Practices

- **Layered Cache**: CDN → reverse proxy (Nginx) → App Cache (Redis) → DB
- **Cache Key**: namespaced, e.g. `user:{id}:profile`
- **TTL**: base + random jitter (prevents cache stampede)
- **Monitoring**: Redis INFO, hit/miss ratio, OOM prevention
- **Persistence**: Redis RDB/AOF depending on durability requirements
