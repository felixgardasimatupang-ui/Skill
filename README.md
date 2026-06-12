# Skill Library

> Kumpulan AI agent skills untuk mempercepat & menstandarisasi software engineering workflows.

## Struktur

```
skills/
├── api-and-interface-design/        ← Project Lifecycle Skills (flat)
├── test-driven-development/         ← 24 skills — fase SDLC
├── ...
├── coding/                          ← Agent Skill Kit
│   ├── ask-bug-finder/              ← 28 coding skills
│   ├── ask-code-reviewer/
│   └── ...
├── planning/                        ← Agent Skill Kit
│   ├── ask-brainstorm/              ← 5 planning skills
│   ├── ask-buildmaster/
│   └── ...
├── tooling/                         ← Agent Skill Kit
│   ├── ask-skill-creator/           ← 9 tooling skills
│   ├── ask-pdf-processing/
│   └── ...
├── manifest.json                    ← Index seluruh ASK skills
└── workflows/                       ← Workflow templates
```

**Total:** 66 skills (24 lifecycle + 42 Agent Skill Kit)

---

## Daftar Skill

### Lifecycle Skills (SDLC Phases)

| Skill | Deskripsi |
|-------|-----------|
| `spec-driven-development` | Buat spesifikasi sebelum coding |
| `planning-and-task-breakdown` | Breakdown tugas dari spesifikasi |
| `incremental-implementation` | Implementasi tipis vertikal |
| `test-driven-development` | Test dulu, implementasi setelah |
| `frontend-ui-engineering` | Komponen UI React |
| `api-and-interface-design` | Desain API dan boundary modul |
| `browser-testing-with-devtools` | Runtime check via browser |
| `debugging-and-error-recovery` | Root cause debugging sistematis |
| `code-review-and-quality` | Review kode 5 sumbu |
| `code-simplification` | Kurangi kompleksitas |
| `security-and-hardening` | OWASP, least privilege |
| `shipping-and-launch` | Deploy aman |
| `git-workflow-and-versioning` | Commit bersih |
| `ci-cd-and-automation` | Quality gates otomatis |
| `deprecation-and-migration` | Migrasi incrementah |
| `documentation-and-adrs` | Dokumentasi dan keputusan arsitektur |
| `doubt-driven-development` | Validasi asumsi sebelum nge-build |
| `using-agent-skills` | Panduan pakai AI agent skills |
| `context-engineering` | Context window optimization |
| `observability-and-instrumentation` | Logging, tracing, monitoring |
| `performance-optimization` | Profiling dan tuning |
| `interview-me` | Sesi wawancara teknis |
| `idea-refine` | Refine ide mentah jadi action |
| `source-driven-development` | Source of truth berbasis kode |

### Coding Skills

| Skill | Versi | Deskripsi |
|-------|-------|-----------|
| `ask-bug-finder` | 1.0.0 | Systematic debugging |
| `ask-code-reviewer` | 1.0.0 | AI code review |
| `ask-commit-assistance` | 1.2.0 | Commit assistance |
| `ask-component-scaffolder` | 1.0.0 | UI component scaffolding |
| `ask-conceptual-integrity-sentinel` | 1.0.0 | Architecture drift audit |
| `ask-db-migration-assistant` | 1.0.0 | Safe DB migrations |
| `ask-docker-best-practices` | 1.0.0 | Docker optimization |
| `ask-docker-expert` | 1.0.0 | Docker expert guidance |
| `ask-effective-llm-coder` | 1.0.0 | LLM-assisted coding |
| `ask-explaining-code` | 1.0.0 | Code explanation |
| `ask-fastapi-architect` | 1.0.0 | FastAPI scaffolding |
| `ask-flutter-architect` | 1.0.0 | Flutter architecture |
| `ask-flutter-mechanic` | 1.0.0 | Flutter maintenance |
| `ask-impact-sentinel` | 1.0.0 | Impact analysis |
| `ask-laravel-architect` | 1.0.0 | Laravel scaffolding |
| `ask-laravel-mechanic` | 1.0.0 | Laravel maintenance |
| `ask-nextjs-architect` | 1.0.0 | Next.js scaffolding |
| `ask-owasp-security-review` | 1.0.0 | OWASP security review |
| `ask-python-refactor` | 1.0.0 | Python refactoring |
| `ask-readme-gardener` | 1.0.0 | README sync |
| `ask-refactoring-readability` | 1.0.0 | Code readability |
| `ask-rest-api-design` | 1.0.0 | REST API design |
| `ask-security-sentinel` | 1.0.0 | Security scanning |
| `ask-shadcn-architect` | 1.0.0 | shadcn/ui components |
| `ask-shadcn-mechanic` | 1.0.0 | shadcn/ui maintenance |
| `ask-unit-test-generation` | 1.0.0 | Unit test generation |
| `ask-vue-architect` | 1.0.0 | Vue 3 scaffolding |
| `ask-vue-mechanic` | 1.0.0 | Vue 3 maintenance |

### Planning Skills

| Skill | Versi | Deskripsi |
|-------|-------|-----------|
| `ask-adr-logger` | 1.0.0 | ADR recording |
| `ask-brainstorm` | 1.0.0 | Structured brainstorming |
| `ask-buildmaster` | 1.0.0 | Epic orchestration |
| `ask-project-memory` | 1.0.0 | Project memory management |
| `ask-solution-architect` | 1.0.0 | Multi-perspective ideation |

### Tooling Skills

| Skill | Versi | Deskripsi |
|-------|-------|-----------|
| `ask-add-agent` | 1.0.0 | AI editor adapter |
| `ask-ast-mapper` | 1.0.0 | AST dependency maps |
| `ask-context-janitor` | 1.0.0 | Token optimization |
| `ask-parallel-auditor` | 1.0.0 | Parallel repo audit |
| `ask-pdf-processing` | 1.0.0 | PDF extraction & forms |
| `ask-skill-capture` | 1.0.0 | Session → skill capture |
| `ask-skill-creator` | 1.0.0 | Skill creation guide |
| `ask-smart-booking-test` | 2.1.0 | E2E booking test |
| `ask-system-architect-prime` | 1.0.0 | System architecture audit |

---

## Struktur Skill

Setiap skill memiliki format standar:

```
ask-bug-finder/
├── SKILL.md           ← Instruksi utama (wajib)
├── skill.yaml         ← Metadata (nama, versi, kategori, tags)
├── README.md          ← Dokumentasi tambahan
├── scripts/           ← Script pendukung
├── tests/             ← Test case / eval
└── assets/            ← Asset pendukung (template, checklist)
```

### Format SKILL.md

```yaml
---
name: ask-bug-finder
description: Systematic debugging dengan reproduction, isolation, dan hypothesis testing.
triggers: ["help find this bug", "debug this error", "why is this failing"]
---
```

### Format skill.yaml

```yaml
name: ask-bug-finder
version: 1.0.0
category: coding
description: Best practices for systematic bug hunting and debugging
tags:
  - debugging
  - bug-hunting
agents:
  - codex
  - gemini
  - claude
```

Lifecycle skills (`skills/` root) hanya memiliki `SKILL.md` dengan frontmatter.

---

## Cara Pakai

### Via opencode (MCP)

Skills sudah terdaftar di `.opencode/opencode.json` dan otomatis dikenali oleh MCP server `ask-skill-kit`.

### Via CLI (ask)

```bash
# Lihat semua skill
ask list

# Filter berdasarkan kategori
ask list --category coding

# Cari skill
ask list --search debugging

# Copy skill ke agent directory
ask copy ask-bug-finder --agent claude
```

### Manual

Buka `skills/<nama-skill>/SKILL.md` dan ikuti instruksi di dalamnya.

---

## Menambahkan Skill Baru

```bash
ask create ask-nama-skill --category coding
```

Atau buat manual dengan struktur folder standar. Update `.opencode/opencode.json` jika perlu.

---

## Kontribusi

1. Fork repo
2. Buat branch: `feat/nama-skill`
3. Commit dengan format: `feat(skill): tambah ask-nama-skill`
4. Push dan buat PR
