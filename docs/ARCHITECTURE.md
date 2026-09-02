# OmniRoute — architektura

<!-- os-status:start -->
**Status:** **43.0** M-50 `china_rail` tablica `/china-rail` (zarchiwizowany). **Etap:** Plan. **Następny:** M-51 Drobnica morska (`/plan-modul`). Nie zgaduj schematu. Nie nowa tabela. Plan: [PLAN-REALIZACJA.md](PLAN-REALIZACJA.md).
<!-- os-status:end --> 
**Kształt:** modularny monolit (Python FastAPI + React Vite SPA)  
**ADR frontend:** [0002](adr/0002-frontend-platform-2026.md) (stack) · [0003](adr/0003-frontend-ui-system-2026.md) (tokeny, wzorce). Makiety: [docs/design/](design/README.md).

## Warstwy

<!-- os-tree:start -->
```
frontend/                 React 19 + Compiler, Vite, TanStack, shadcn, PostHog
  src/features/           bank-payment · bookkeeping · cash-flow · channel-quotes · charge-codes · charges · china-rail · commodity-codes · cost-to-serve · credit-reviews · customer-sops · dangerous-goods · edi-message · extraction · finance-board · fx-difference · geography · intermodal-rail · mail-integration · money-cost · nbp-rates · networks · operational-exception · operator-notice · ops · organization-settings · parties · party-scorecards · port-surcharges · quotations · quote-invoice-settlement · rate-lines · road-transport · sales-invoice · session · shipment · shipment-document · tenancy · tracking
  src/components/ui/      shadcn
  src/components/data-table/  DataTableShell (Golden Standard)
backend/app/
  api/             routery, DTO, require_permission — bez logiki
  services/        channel_quotes · charge_codes · charges · commodity_codes · dangerous_goods · extraction · geography · nbp_rates · networks · organization_settings · parties · port_surcharges · quotations · rate_lines · tenancy
  repositories/    dostęp SQL
  models/          SQLAlchemy
  domain/          typy, wyjątki, Money
  ai_transforms/   ekstrakcja → JSON (stateless, HITL)
  workflows/       Temporal (wizja — nie działający system)
  integrations/    OpenFGA, docling, langfuse (trace przy extract; no-op bez kluczy)
authz/             model.fga (źródło prawdy AuthZ)
```
<!-- os-tree:end -->

## Granice

- import-linter: warstwy + niezależność BC.
- Multi-tenancy: RLS PostgreSQL + OpenFGA na API.
- AI: extract only; zapis przez `service` + HITL.
- Tabele UI: wyłącznie DataTableShell — drugi grid engine wymaga ADR.

## Integracje

PostgreSQL 16 · OpenFGA · Langfuse (trace, no-op bez kluczy) · PostHog  
**(cel, nie runtime):** Redis · MinIO · Temporal · Hatchet · EmailEngine

## Dokumentacja

- Stan: `docs/state/CURRENT.md`
- ADR: `docs/adr/`
- Spec: `docs/spec/`
- Knowledge (retrieve, nie dump): `docs/_knowledge/`
- Archiwum: `Informacje z claude/` — **nie ładować hurtowo do kontekstu agenta**
