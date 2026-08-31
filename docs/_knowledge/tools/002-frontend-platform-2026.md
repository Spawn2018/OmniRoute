# Frontend platform 2026 — kanon OmniRoute

**ADR:** [docs/adr/0002-frontend-platform-2026.md](../../adr/0002-frontend-platform-2026.md)

## Stack (Adopt)

- React 19 + React Compiler · Vite · TanStack Router/Query/Form/Table/Virtual
- shadcn/ui + Tailwind v4 + Radix · @dnd-kit · PostHog
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

## Źródła

Thoughtworks Radar 2026-04 (React Adopt, TanStack Start Assess) · State of React/JS 2025 · NN/G complex apps · Pencil & Paper data tables · TanStack Column DnD docs
