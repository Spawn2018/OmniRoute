# OmniRoute — architektura

<!-- os-status:start -->
**Status:** **120.0** S27b karta z decyzji oferty (M-13). **Etap:** Plan. **Następny:** `/plaster` **121.0** — leftover S11 `changed` na `operator_decision`. Nie accept extractu. Nie F9.1. Plan: [PLAN-REALIZACJA.md](PLAN-REALIZACJA.md).
<!-- os-status:end --> 
**Kształt:** modularny monolit (Python FastAPI + React Vite SPA)  
**ADR frontend:** [0002](adr/0002-frontend-platform-2026.md) (stack) · [0003](adr/0003-frontend-ui-system-2026.md) (tokeny, wzorce). Makiety: [docs/design/](design/README.md).

## C4

Context: operator pracuje w jednym produkcie; baza i uprawnienia są osobnymi systemami. LLM jest na zewnątrz i **nie zapisuje** stawek.

```mermaid
C4Context
title OmniRoute — context
Person(operator, "Operator", "spedytor tenanta")
System(omniroute, "OmniRoute", "katalogi, wyceny, HITL")
System_Ext(pg, "PostgreSQL", "RLS, Decimal")
System_Ext(fga, "OpenFGA", "uprawnienia API")
System_Ext(llm, "Model językowy", "szkic extractu, nie stawka")
Rel(operator, omniroute, "joby zapisu i recenzja HITL")
Rel(omniroute, pg, "SQL")
Rel(omniroute, fga, "check")
Rel(omniroute, llm, "extract; human-in-the-loop")
```

Container: SPA i API w jednym repozytorium, dwa procesy. Temporal / outbox — cel, nie runtime.

```mermaid
C4Container
title OmniRoute — container
Person(operator, "Operator")
Container(spa, "SPA", "React + Vite", "ekrany jobów")
Container(api, "API", "FastAPI", "serwisy BC")
ContainerDb(pg, "PostgreSQL", "RLS + Numeric")
Container(fga, "OpenFGA", "model.fga")
Rel(operator, spa, "HTTPS")
Rel(spa, api, "JSON / OpenAPI")
Rel(api, pg, "SQL")
Rel(api, fga, "check")
```

## Warstwy

<!-- os-tree:start -->
```
frontend/                 React 19 + Compiler, Vite, TanStack, shadcn, PostHog
  src/features/           ai-copilot · bank-payment · bookkeeping · cargo-claim · cash-flow · channel-quotes · charge-codes · charges · china-rail · commodity-codes · cost-to-serve · credit-reviews · customer-sops · dangerous-goods · edi-message · extraction · extraction-quality · finance-board · fraud-flag · fx-difference · gdpr · geography · intermodal-rail · mail-integration · money-cost · nbp-rates · networks · observability · ocean-lcl · operational-exception · operator-decisions · operator-notice · ops · organization-settings · outbox · parties · party-scorecards · port-surcharges · quotations · quote-invoice-settlement · rate-lines · road-transport · sales-invoice · sanctions · session · shipment · shipment-document · tenancy · tenant-rollout · tracking · watchtower
  src/components/ui/      shadcn
  src/components/data-table/  DataTableShell (Golden Standard)
backend/app/
  api/             routery, DTO, require_permission — bez logiki
  services/        bank_payments · bookkeeping · cargo_claims · carrier_inquiries · cash_flows · channel_quotes · charge_codes · charges · collective_invoices · commodity_codes · cost_to_serve · customer_rfqs · dangerous_goods · edi_messages · extraction · fraud_flags · fx_differences · gdpr_requests · geography · inbound_messages · mail_drafts · money_costs · nbp_rates · networks · operational_exceptions · operator_decisions · operator_notices · organization_settings · outbox_events · parties · port_surcharges · quotations · quote_invoice_settlements · rate_lines · sales_invoices · shipment_documents · shipment_legs · shipments · tenancy · tracking_events
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
