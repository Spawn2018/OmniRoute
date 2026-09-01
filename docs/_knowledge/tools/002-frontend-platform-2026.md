# Frontend platform 2026 — kanon OmniRoute

**ADR:** [0002](../../adr/0002-frontend-platform-2026.md) (stack) · [0003](../../adr/0003-frontend-ui-system-2026.md) (tokeny, wzorce, HITL/tenant). Makiety: [docs/design/](../../design/README.md).

## Stack (Adopt)

- React 19 + React Compiler · Vite · TanStack Router/Query/Form/Table/Virtual
- shadcn/ui + Tailwind v4 + **Radix** (pin `components.json`; Base UI tylko nowym ADR) · @dnd-kit · PostHog
- Tokeny: OKLCH luminance-first + dark (leftover U-oklch-dark). Condensed tylko na gridzie stawek.
- Referencja layoutu: satnaing/shadcn-admin (wzorce, nie fork)

## DataTableShell (Golden Standard)

Każda lista biznesowa:

1. Toolbar: search, faceted filters, density, ViewManager
2. ColumnEditor: checkbox visibility + DnD order (`columnVisibility` + `columnOrder`)
3. Persist: `table_view` (RLS) — JSON order/visibility/filters/sorting/density
4. Table: sticky header, pin, virtual >500 rows, `<Money/>`
5. Telemetria: `table_view_*`, `filter_*`, `command_palette_used`

## Anti AI-slop

Neutral tokens, compact, `rounded-md`, zero fioletowych gradientów / landing hero w ops UI.

## Utrzymanie kontraktu (spłacone — nie wrzucaj z powrotem do długu)

- openapi-ts: `just api-types` → `frontend/src/api/` (gate = typecheck, nie regen)
- PostHog: lazy `dynamic import("posthog-js")` — nie w main chunk
- vitest: minimum na DataTableShell; kolejka ekstrakcji bez vitest
- Gate vs DoD: `docs/PLAN-REALIZACJA.md`

## Dług pozostały

- auth localStorage / JWT — poza zakresem B.5/B.6
- flatten `ExtractRequest` anyOf|null — cast w wrapperze, nie ręczny edit `src/api/*`

## Źródła

Thoughtworks Radar 2026-04 (React Adopt, TanStack Start Assess) · State of React/JS 2025 · NN/G complex apps · Pencil & Paper data tables · TanStack Column DnD docs
