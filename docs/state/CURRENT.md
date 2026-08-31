# Bieżący focus

**Faza:** B — DataTableShell  
**Repo:** https://github.com/Spawn2018/OmniRoute (`main`)  
**Następny krok:** push **0.6** + green CI → B.7 / slot jakości

**Plan:** [docs/PLAN-REALIZACJA.md](docs/PLAN-REALIZACJA.md)  
**ADR:** [docs/adr/0002-frontend-platform-2026.md](docs/adr/0002-frontend-platform-2026.md)

---

# Plaster 0.6 — DataTableShell

**Delta:** [docs/deltas/open/0.6-datatable-views.md](docs/deltas/open/0.6-datatable-views.md)  
**Status:** lokalnie gotowy — commit/push

## Dostarczone
`table_view` RLS + API CRUD + OpenFGA `can_manage_table_views` · DataTableShell (ColumnEditor DnD, ViewManager, virtual, filtry) · consumer `tenancy.users` · vitest

## Poza zakresem / później
openapi-ts · cov-fail-under / jscpd · lazy PostHog · B.7 Pro · JWT · Faza C

---

## Następne (bez kolizji)
1. Green CI dla 0.6  
2. B.7 lub procedura ręczna  
3. Slot jakości (openapi-ts, cov, jscpd)  
4. Faza C
