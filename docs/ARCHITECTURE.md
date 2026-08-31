# OmniRoute — architektura

**Status:** Faza C (B + C.1–C.5 + 0.11–0.15 leftover + D minimal DONE; następny: D0 OS, nie OAuth)  
**Kształt:** modularny monolit (Python FastAPI + React Vite SPA)  
**ADR frontend:** [0002-frontend-platform-2026](adr/0002-frontend-platform-2026.md)

## Warstwy

```
frontend/                 React 19 + Compiler, Vite, TanStack, shadcn, PostHog
  src/features/<moduł>/   ekrany, hooki, testy (tenancy, extraction, session)
  src/components/ui/      shadcn
  src/components/data-table/  DataTableShell (Golden Standard)
backend/app/
  api/             routery, DTO, require_permission — bez logiki
  services/<bc>/   logika domenowa (tenancy, extraction)
  repositories/    dostęp SQL
  models/          SQLAlchemy
  domain/          typy, wyjątki, Money
  ai_transforms/   ekstrakcja → JSON (stateless, HITL)
  workflows/       Temporal (wizja — nie działający system)
  integrations/    OpenFGA, docling, langfuse (trace przy extract; no-op bez kluczy)
authz/             model.fga (źródło prawdy AuthZ)
```

## Granice

- import-linter: warstwy + niezależność BC.
- Multi-tenancy: RLS PostgreSQL + OpenFGA na API.
- AI: extract only; zapis przez `service` + HITL.
- Tabele UI: wyłącznie DataTableShell — drugi grid engine wymaga ADR.

## Integracje

PostgreSQL 16 · OpenFGA · (plan) Redis · MinIO · Temporal · Hatchet · EmailEngine · Langfuse · PostHog

## Dokumentacja

- Stan: `docs/state/CURRENT.md`
- ADR: `docs/adr/`
- Spec: `docs/spec/`
- Knowledge (retrieve, nie dump): `docs/_knowledge/`
- Archiwum: `Informacje z claude/` — **nie ładować hurtowo do kontekstu agenta**
