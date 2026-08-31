# Bieżący focus

**Faza:** B — DataTableShell  
**Repo:** https://github.com/Spawn2018/OmniRoute (`main` @ `c985089`)  
**Następny krok:** plaster **0.6 DataTableShell** (po green CI dla 0.5)

**Plan:** [docs/PLAN-REALIZACJA.md](docs/PLAN-REALIZACJA.md) (§ Gate dziś vs DoD)  
**ADR:** [docs/adr/0001-cursor-software-factory-weryfikacja.md](docs/adr/0001-cursor-software-factory-weryfikacja.md) · [docs/adr/0002-frontend-platform-2026.md](docs/adr/0002-frontend-platform-2026.md)

---

# Plaster 0.5 — Frontend Shell 2026

**Delta:** [docs/deltas/archived/0.5-frontend-shell.md](docs/deltas/archived/0.5-frontend-shell.md)  
**Status:** **wypchnięty** (`c985089`) — czekamy na green CI

---

# Plaster 0.6 — DataTableShell (AKTYWNY po green CI)

**Delta:** [docs/deltas/open/0.6-datatable-views.md](docs/deltas/open/0.6-datatable-views.md)

## Kolejność implementacji (jeden pion)
1. Migracja `table_view` + RLS + test izolacji  
2. Model → repo → service → API CRUD (+ OpenFGA)  
3. Frontend: DataTableShell + ColumnEditor + ViewManager  
4. Consumer `tenancy.users`  
5. vitest minimum · (openapi-ts jeśli mieści się)  
6. PostHog events

## Poza zakresem
cov/jscpd w gate, B.7 Pro, JWT, Faza C

---

## Następne po 0.6
B.7 (gdy Pro/public) · slot jakości · Faza C · Faza D
