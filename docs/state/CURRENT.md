# Bieżący focus

**Faza:** B — domknięcie frontendu (po RLS + OpenFGA)  
**Repo:** https://github.com/Spawn2018/OmniRoute (`main`)  
**Następny krok:** plaster **0.5 Frontend Shell 2026** → potem **0.6 DataTableShell**

**Plan:** [docs/PLAN-REALIZACJA.md](PLAN-REALIZACJA.md)  
**ADR:** [0001](adr/0001-cursor-software-factory-weryfikacja.md) · [0002 Frontend 2026](adr/0002-frontend-platform-2026.md)

---

# Plaster 0.5 — Frontend Shell 2026

**Delta:** [docs/deltas/open/0.5-frontend-shell.md](docs/deltas/open/0.5-frontend-shell.md)  
**Status:** **następny do realizacji**

## Zakres (skrót)
Vite + React 19/Compiler + TanStack Router/Query/Form + shadcn + tokens + ⌘K + PostHog.

## Poza zakresem
ColumnEditor / `table_view` (to 0.6), Faza C AI.

---

# Plaster 0.6 — DataTableShell (kolejny)

**Delta:** [docs/deltas/open/0.6-datatable-views.md](docs/deltas/open/0.6-datatable-views.md)  
Filtry, widoki, checkbox + DnD kolumn, persist RLS — Golden Standard dla wszystkich list.

---

## Ukończone

| Faza | Co |
|---|---|
| 0–A.5 | GitHub, Cursor OS, MCP |
| B.2–B.4 | RLS, pełny gate, OpenFGA |
| ADR-0002 | Frontend platform 2026 (źródła Thoughtworks / SoR / NN/G) |

## Następne (kolejność bez kolizji)

1. **0.5** Frontend Shell  
2. **0.6** DataTableShell + `table_view`  
3. **B.7** Branch protection (po green CI)  
4. **Faza C** AI (HITL na gęstym UI)  
5. **Faza D** Automations / agentlint
