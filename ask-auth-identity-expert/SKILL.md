---
name: ask-auth-identity-expert
description: Mengaudit alur otentikasi ketat (OAuth2, MFA, rotasi token, dan Role-Based Access Control/RBAC).
triggers: ["auth audit", "oauth2", "jwt security", "mfa", "rbac", "token rotation", "login flow", "authentication"]
---

# Auth & Identity Expert

Mengaudit dan memperkuat alur otentikasi, otorisasi, dan manajemen identitas.

<critical_constraints>
- ❌ NO menyimpan JWT di localStorage (XSS vulnerable)
- ❌ NO hardcoded secrets / API keys di kode
- ❌ NO bypass otorisasi — EVERY request wajib dicek
- ✅ WAJIB httpOnly cookie untuk refresh token
- ✅ WAJIB rate limiting di endpoint login/register
- ✅ WAJIB minimum password complexity (12+ chars, mixed case, number, symbol)
- ✅ WAJIB MFA untuk admin / privileged actions
</critical_constraints>

<heuristics>
- Login tanpa rate limiting → tambah rate limiter + account lockout
- Token tanpa expiry / refresh → implementasi short-lived access token (15 menit) + refresh token (7 hari)
- Role hanya di token, tidak dicek di DB → dual check: token + DB
- Password disimpan tanpa hashing → bcrypt / argon2
- Tidak ada CSRF protection di cookie auth → double-submit cookie / SameSite=Strict
- Logout tidak invalidate token → maintain token blacklist di Redis
</heuristics>

## Purpose

Memastikan sistem autentikasi dan otorisasi memenuhi standar keamanan industri: OWASP ASVS, NIST, dan best practices modern.

## Usage

Gunakan ketika:
- Mendesain atau mengaudit alur login/register
- Implementasi OAuth2 / SSO
- Setup RBAC / permission system
- Menambahkan MFA
- Melakukan penetration test / security audit
- Rotasi token atau migrasi auth provider

### Core Protocol

1. **Authentication Flow**: Email/password → verify → issue tokens
2. **Token Strategy**: Access (15m, in-memory) + Refresh (7d, httpOnly cookie)
3. **Authorization**: RBAC/ABAC — check di middleware per request
4. **MFA**: TOTP (Google Authenticator) atau SMS/Email OTP
5. **Audit Log**: Log semua login attempt, role change, permission change

## Examples

### Token Rotation
```ts
async function rotateTokens(refreshToken: string) {
  const stored = await db.refreshToken.findUnique({ where: { token: refreshToken } })
  if (!stored || stored.expiresAt < new Date()) throw new UnauthorizedError()

  await db.refreshToken.delete({ where: { id: stored.id } })

  const newAccess = signJwt({ userId: stored.userId }, '15m')
  const newRefresh = crypto.randomUUID()
  await db.refreshToken.create({ data: { token: newRefresh, userId: stored.userId, expiresAt: addDays(7) } })

  return { accessToken: newAccess, refreshToken: newRefresh }
}
```

### RBAC Middleware
```ts
function requireRole(...roles: string[]) {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' })
    }
    next()
  }
}
```

## Best Practices

- **Password Strength**: zxcvbn validation di frontend + backend
- **Session Management**: Rotate session ID setelah login
- **MFA Recovery**: Berikan backup codes (single-use)
- **Rate Limit**: Login: 5 attempts/menit, Register: 2/jam/IP
- **Audit Trail**: Simpan user agent, IP, timestamp untuk setiap auth event
- **Account Lockout**: 15 menit setelah 5 failed attempts
