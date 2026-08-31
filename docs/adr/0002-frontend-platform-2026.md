# ADR-0002: Frontend platform 2026 — Vite SPA + TanStack + DataTableShell

**Status:** przyjęta  
**Data:** 2026-08-31  
**Moduły:** M-01+ (wszystkie UI), platforma  
**Zastępuje ustalenia:** placeholder `frontend/src/main.tsx`; luźne „RHF vs TanStack Form”; odkładanie branch protection wyłącznie do Fazy D

## Kontekst

Po Fazie B (RLS + OpenFGA) brakuje produkcyjnego frontendu. Wymagania operatora:
- zero AI-slopu, wygląd enterprise up-to-date,
- tabele z filtrami, zapisem widoków, widocznością i kolejnością kolumn (checkbox + DnD),
- zgodność ze stosem i praktykami dużych software house’ów 2025–26,
- brak długu technologicznego i kolizji z planem backendu.

## Decyzja

### Stack (Adopt / Assess — źródła poniżej)

| Warstwa | Wybór | Werdykt |
|---|---|---|
| UI library | **React 19 + React Compiler** (Vite) | Thoughtworks Radar **Adopt** (15.04.2026) |
| Bundler | **Vite** | Thoughtworks **Adopt** (IV 2025); State of JS 2025 — top loved/used |
| App shape | **SPA wewnętrzna** (nie SSR-first) | State of React 2025: SPA ~84,5% usage |
| Routing | **TanStack Router** | type-safe; ekosystem TanStack |
| Server state | **TanStack Query** | State of React 2025: ~68% usage |
| Forms | **TanStack Form + Zod** | spójność stacku; zamiast RHF (unikamy dwóch konwencji) |
| Tables | **TanStack Table + Virtual** | headless; gęstość pod kontrolą |
| Column DnD | **@dnd-kit** | oficjalny przykład TanStack Column DnD |
| Components | **shadcn/ui + Tailwind v4 + Radix** | kod w repo; design system egzekwowalny |
| Referencja layoutu | `satnaing/shadcn-admin` (wzorce, nie fork produktu) | gęsty admin Vite+TanStack Router |
| Telemetria UX | **PostHog** od dnia 1 shella | plan + pomiar adoption widoków/filtrów |
| Full-stack meta | **TanStack Start — NIE teraz** | Thoughtworks Radar **Assess** (15.04.2026); SSR zbędne dla app wewnętrznej |

### Architektura UI

1. **Design tokens** (CSS variables) — człowiek zatwierdza raz; agent nie inventuje palety.
2. **DataTableShell** — jeden Golden Standard dla wszystkich list:
   - faceted filters + URL sync,
   - ColumnEditor (checkbox visibility + DnD order),
   - ViewManager (zapis/odczyt/import widoku),
   - density compact/comfortable,
   - sticky header, pin, virtualizacja >500 wierszy.
3. **Persistencja widoków** — tabela `table_view` z RLS (`organization_id` + `user_id` + `table_key` + JSON), nie sam localStorage.
4. **Command palette** (⌘K / Ctrl+K) — nawigacja + akcje (standard SaaS 2026).
5. **Progressive disclosure** (NN/G) — zaawansowane filtry/konfiguracja kolumn w panelu drugiego poziomu; operacyjna gęstość na pierwszym.

### Anti-collision / anti-debt

- Zakaz drugiego grid engine (Ag Grid / MUI DataGrid) bez ADR.
- Zakaz Next.js jako primary app wewnętrznej (potwierdzone: polarizacja SoJS 2025; plan odrzuca).
- Zakaz ThemeForest / „AI dashboard” templates.
- Frontend nie omija OpenFGA/RLS — tożsamość JWT Bearer (`sub`/`org`); OpenFGA = AuthZ.

## Konsekwencje

- Plaster **B.5** = shell + tokens + PostHog + ⌘K.
- Plaster **B.6** = DataTableShell + `table_view` + ColumnEditor na `tenancy.users`.
- Branch protection na `main` = **po green gate B**, nie czekać na Fazę D.
  **Uwaga operacyjna:** GitHub Free + private → API protection HTTP 403;
  wymaga Pro/Team/public albo procedury ręcznej (patrz PLAN B.7).
- Faza C.1–C.5 **zrobiona**; UI = kolejka DataTableShell + split-screen HITL (0.13). 0.12 JWT hello **zrobiony**. Następny leftover: HTTP happy-path extract/accept.
- Uczciwość DoD/gate (stub vs real): `docs/PLAN-REALIZACJA.md` § Gate dziś.

## Źródła (nie plotki)

| Źródło | Data / ID | Wniosek użyty |
|---|---|---|
| [Thoughtworks Radar — React JS](https://www.thoughtworks.com/radar/languages-and-frameworks/react-js) | 15.04.2026 Adopt | React 19 + Compiler |
| [Thoughtworks Radar — Vite](https://www.thoughtworks.com/radar/tools) | IV 2025 Adopt | Vite jako bundler |
| [Thoughtworks Radar — TanStack Start](https://www.thoughtworks.com/radar/languages-and-frameworks/tanstack-start) | 15.04.2026 Assess | Start odroczony |
| [State of React 2025](https://strapi.io/blog/state-of-react-2025-key-takeaways) (Devographics, XI 2025–I 2026) | SPA 84,5%; Query ~68% | SPA + TanStack Query |
| [State of JS 2025 Libraries](https://2025.stateofjs.com/en-US/libraries/) | Vite top loved/used | Vite |
| [NN/G — Complex applications](https://www.nngroup.com/articles/strategies-complex-application-design/) | evergreen / aktualne | research + progressive disclosure |
| [NN/G — Heuristics for complex apps](https://www.nngroup.com/articles/usability-heuristics-complex-applications/) | staged disclosure | ColumnEditor / advanced filters |
| [Pencil & Paper — Enterprise data tables](https://www.pencilandpaper.io/articles/ux-pattern-analysis-enterprise-data-tables) | industry UX | column show, density, filters |
| [TanStack Table — Column ordering / DnD](https://tanstack.com/table/latest/docs/framework/react/examples/column-dnd) | docs | @dnd-kit |
| Plan OmniRoute + `ui-design-system.mdc` | 2026-08 | anti AI-slop, density |

## Alternatywy odrzucone

| Alternatywa | Dlaczego |
|---|---|
| Next.js App Router primary | SoJS: polarizacja; Thoughtworks Trial historycznie; plan odrzuca SSR dla app wewnętrznej |
| TanStack Start already | Radar **Assess** — za wcześnie na fundament produkcyjny |
| RHF + TanStack Form jednocześnie | dwie konwencje = dług |
| Fork całego shadcn-admin | śmieci demo-pages; bierzemy wzorce |
| localStorage-only views | brak multi-device / multi-tenant audit |
