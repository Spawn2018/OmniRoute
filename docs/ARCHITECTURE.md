# OmniRoute — architektura

**Status:** Faza B (backend Golden Standard done; frontend shell = następny)  
**Kształt:** modularny monolit (Python FastAPI + React Vite SPA)  
**ADR frontend:** [0002-frontend-platform-2026](adr/0002-frontend-platform-2026.md)

## Warstwy

```
frontend/                 React 19 + Compiler, Vite, TanStack, shadcn, PostHog
  src/features/<moduł>/   ekrany, hooki, testy
  src/components/ui/      shadcn
  src/components/data-table/  DataTableShell (Golden Standard)
backend/app/
  api/             routery, DTO, require_permission — bez logiki
  services/        logika domenowa
  repositories/    dostęp SQL
  models/          SQLAlchemy
  domain/          typy, wyjątki, Money
  workflows/       Temporal
  integrations/    OpenFGA, adaptery zewnętrzne
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
