---
name: ask-e2e-test-generator
description: Membuat skrip pengujian ujung-ke-ujung (E2E) otomatis menggunakan Playwright atau Cypress berdasarkan simulasi perilaku pengguna nyata.
triggers: ["e2e test", "playwright", "cypress", "user flow test", "integration test", "browser test"]
---

# E2E Test Generator

Membuat skrip E2E test yang komprehensif dengan mensimulasikan alur pengguna nyata.

<critical_constraints>
- ❌ NO test tanpa assertion — setiap aksi harus diverifikasi
- ❌ NO hardcoded selector — gunakan data-testid / semantic locator
- ❌ NO test dependen — setiap test harus standalone
- ✅ WAJIB mock API eksternal (third-party) — jangan dependen
- ✅ WAJIB reset state sebelum setiap test
- ✅ WAJIB handle loading states (waitForSelector, waitForResponse)
- ✅ WAJIB screenshot on failure untuk debugging
</critical_constraints>

<heuristics>
- Login flow → test happy path + wrong password + email not found
- CRUD feature → create → read → update → delete
- Form submission → valid data + invalid data + empty field
- Pagination → page 1, page 2, last page, empty result
- Search/filter → exact match, partial match, no result
- File upload → valid file, oversized file, wrong format
- Error states → 403, 500, network offline
</heuristics>

## Purpose

Mengotomatisasi pengujian alur pengguna kritis untuk menangkap regression sebelum rilis.

## Usage

Gunakan ketika:
- Menambahkan fitur baru dengan alur pengguna kompleks
- Sebelum rilis — regression test untuk critical path
- Setup CI/CD pipeline — gate untuk deployment
- Refactor besar — memastikan existing flow tidak rusak

### Core Protocol

1. **Map User Flow**: Daftar langkah dari awal sampai selesai
2. **Identify Selectors**: Gunakan `data-testid` atau semantic attributes
3. **Write Test**: Happy path first, then edge cases
4. **Handle Async**: Wait for elements, network requests, animations
5. **Verify**: Assertions on UI state, URL, toast messages, data
6. **Cleanup**: Reset DB state / logout

## Examples

### Playwright — Login Flow
```ts
import { test, expect } from '@playwright/test'

test('login with valid credentials', async ({ page }) => {
  await page.goto('/login')
  await page.fill('[data-testid="email"]', 'user@example.com')
  await page.fill('[data-testid="password"]', 'correct-password')
  await page.click('[data-testid="login-btn"]')

  await expect(page).toHaveURL('/dashboard')
  await expect(page.locator('[data-testid="user-name"]')).toHaveText('John Doe')
})

test('login with wrong password shows error', async ({ page }) => {
  await page.goto('/login')
  await page.fill('[data-testid="email"]', 'user@example.com')
  await page.fill('[data-testid="password"]', 'wrong-password')
  await page.click('[data-testid="login-btn"]')

  await expect(page.locator('[data-testid="error-msg"]')).toBeVisible()
  await expect(page.locator('[data-testid="error-msg"]')).toContainText('Invalid credentials')
})
```

### Cypress — CRUD Flow
```ts
describe('Student CRUD', () => {
  beforeEach(() => {
    cy.loginAsAdmin()
    cy.visit('/students')
  })

  it('creates a new student', () => {
    cy.get('[data-testid="add-student-btn"]').click()
    cy.get('[data-testid="name-input"]').type('Budi Santoso')
    cy.get('[data-testid="email-input"]').type('budi@example.com')
    cy.get('[data-testid="save-btn"]').click()
    cy.get('[data-testid="student-table"]').should('contain', 'Budi Santoso')
  })

  it('deletes a student', () => {
    cy.get('[data-testid="delete-btn"]').first().click()
    cy.get('[data-testid="confirm-delete"]').click()
    cy.get('[data-testid="student-table"]').should('not.contain', 'Budi Santoso')
  })
})
```

## Best Practices

- **Data-testid**: `[data-testid="element-name"]` — hindari CSS class / XPath
- **Page Object Model**: Pisahkan locators ke page classes
- **Test Isolation**: Gunakan `beforeEach` untuk reset
- **CI Integration**: Jalankan di CI dengan `--headed` hanya saat debug
- **Fixtures**: Gunakan test fixtures untuk data factory
- **Reporting**: HTML reporter + trace viewer (Playwright) / video (Cypress)
