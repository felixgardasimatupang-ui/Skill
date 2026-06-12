---
name: ask-data-privacy-compliance
description: Menjamin enkripsi data sensitif tingkat kolom dan sanitasi log dari kebocoran PII.
triggers: ["pii", "gdpr", "data privacy", "encrypt column", "log sanitization", "data compliance", "sensitive data"]
---

# Data Privacy & Compliance

Melindungi data sensitif pengguna dengan enkripsi, masking, dan sanitasi di semua lapisan.

<critical_constraints>
- ❌ NO logging PII (email, phone, KTP, alamat) plaintext
- ❌ NO menyimpan password / API key tanpa hashing
- ❌ NO mengirim PII via URL parameter
- ✅ WAJIB enkripsi kolom sensitif di database (AES-256-GCM)
- ✅ WAJIB masking PII di logs (email → `j***@example.com`)
- ✅ WAJIB purge policy untuk data pribadi setelah retention period
</critical_constraints>

<heuristics>
- Log mengandung email → replace dengan hash/pattern
- API response mengandung NIK/KTP → mask middle digits (123****89)
- Cookie menyimpan identitas → encrypt value
- Ekspor data (GDPR Art. 20) → format machine-readable (JSON)
- Hapus akun (right to erasure) → soft delete + scheduled purge
- Third-party API → verifikasi data minimization (kirim minimal data)
</heuristics>

## Purpose

Memastikan aplikasi memenuhi regulasi privasi (GDPR, UU PDP, CCPA) dengan melindungi data sensitif dari kebocoran di database, logs, dan response API.

## Usage

Gunakan ketika:
- Mendesain schema database dengan data sensitif
- Membuat logs / audit trail
- Mengirim data ke third-party API
- Implementasi fitur "Hapus Akun" atau "Ekspor Data"
- Code review untuk security/privacy
- Persiapan audit compliance

### Core Protocol

1. **Identifikasi PII**: Tandai field sensitif (email, phone, KTP, alamat, kesehatan, keuangan)
2. **Encrypt at Rest**: AES-256-GCM untuk kolom sensitif di DB
3. **Mask in Logs**: Pattern-based replacement sebelum logging
4. **Data Minimization**: Hanya collect & expose data yang diperlukan
5. **Retention & Deletion**: Tentukan retention period + purge policy

## Examples

### Column Encryption (Prisma + middleware)
```ts
prisma.$use(async (params, next) => {
  if (params.model === 'User' && params.action === 'create') {
    params.args.data.email = encrypt(params.args.data.email)
    params.args.data.phone = encrypt(params.args.data.phone)
  }
  const result = await next(params)
  if (params.model === 'User' && params.action === 'findUnique') {
    result.email = decrypt(result.email)
    result.phone = decrypt(result.phone)
  }
  return result
})
```

### Log Sanitization
```ts
const PII_PATTERNS = [
  /\b[\w.-]+@[\w.-]+\.\w+\b/g,                    // email
  /\b\d{16}\b/g,                                    // credit card
  /\b(\d{1,3}\.){3}\d{1,3}\b/g,                    // IP address
  /\b\d{6,}\b/g,                                    // NIK/KTP
]

function sanitizeLog(msg: string): string {
  for (const pattern of PII_PATTERNS) {
    msg = msg.replace(pattern, '***')
  }
  return msg
}
```

### Right to Erasure (GDPR)
```ts
async function deleteUser(userId: string) {
  await prisma.user.update({
    where: { id: userId },
    data: {
      email: `deleted-${userId}@anon.local`,
      name: 'Deleted User',
      phone: null,
      deletedAt: new Date(),
    }
  })
  // Anonymize related records
  await prisma.auditLog.updateMany({
    where: { userId },
    data: { userId: null }
  })
}
```

## Best Practices

- **Encryption Key**: Gunakan KMS (AWS KMS / GCP Cloud KMS) — jangan hardcode
- **Encryption Rotation**: Rotate key setiap 90 hari
- **Data Classification**: Public → Internal → Confidential → Restricted
- **Log Levels**: Jangan log data sensitif di DEBUG/INFO, hanya di ERROR dengan sanitasi
- **Consent**: Simpan preferensi consent user (GDPR Art. 7)
- **DPIA**: Lakukan Data Protection Impact Assessment untuk fitur baru
