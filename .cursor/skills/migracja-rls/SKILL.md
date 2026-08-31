---
name: migracja-rls
description: Dodanie tabeli z izolacją tenantów i testem dowodzącym
---

# Tabela z RLS

## Migracja (wzorzec)

- `organization_id UUID NOT NULL REFERENCES organization(id)`
- `ENABLE ROW LEVEL SECURITY` + `FORCE ROW LEVEL SECURITY`
- Polityka: `organization_id = current_setting('app.current_org')::uuid`
- Indeks na `organization_id`

## Test obowiązkowy

Skopiuj wzorzec z `tests/patterns/tenant_isolation.py`.
Bez tego testu plaster nie jest ukończony.

## Plaster 0.3 — exemplar, nie WIP

0.3 jest **ukończony**. Kopiuj wzorzec (`organization`, `app_user`, test izolacji)
przy nowej tabeli. Bieżący plaster: `docs/state/CURRENT.md`.
Delta: `docs/deltas/archived/0.3-tenancy.md`.
