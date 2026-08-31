# OmniRoute — architektura (szkic)

**Status:** bootstrap Faza A  
**Kształt:** modularny monolit (Python FastAPI + React Vite SPA)

## Warstwy

```
frontend/          React 19, Vite, TanStack, shadcn
backend/app/
  api/             routery, DTO — bez logiki
  services/        logika domenowa
  repositories/    dostęp SQL
  models/          SQLAlchemy
  domain/          typy, wyjątki, Money
  workflows/       Temporal
  integrations/    adaptery armatorów, email, KSeF
```

## Granice

- import-linter egzekwuje warstwy i niezależność modułów domenowych.
- Multi-tenancy: RLS w PostgreSQL, nie konwencja aplikacyjna.
- AI: warstwa stateless (extract); zapis deterministyczny w services.

## Integracje (plan)

PostgreSQL 16 · Redis · MinIO · Temporal · Hatchet · OpenFGA · EmailEngine · Langfuse

## Dokumentacja źródłowa

Pełna specyfikacja modułów: `Informacje z claude/REJESTR-MODULOW-I-PLAN-v2.md`  
Decyzje: `docs/adr/` + `Informacje z claude/OmniRoute-dokumentacja/docs/07-projekt/DECISIONS.md`
