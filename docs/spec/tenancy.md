# Plaster 0.3 — M-01 Wielodostępność

## Zakres
- Tabele `organization`, `app_user`
- RLS FORCE na obu tabelach
- Polityka: `current_setting('app.current_org')`
- Test izolacji: `backend/tests/patterns/tenant_isolation.py`

## Kryteria akceptacji
- Migracja up/down
- Test izolacji green
- Repozytoria filtrują przez RLS (brak jawnego organization_id w SELECT — kontekst sesji)

## Poza zakresem
OpenFGA, UI admin, billing.
