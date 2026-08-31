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
OpenFGA (0.4), UI admin, billing, IdP/OIDC.

## Sesja JWT (0.12)

- `POST /api/v1/session/token` — hello: `organization_id` + `user_id` z `app_user` (bez hasła)
- `GET /api/v1/session/me` — claims z Bearer
- Tożsamość wyłącznie z JWT (`sub`, `org`). OpenFGA = autoryzacja. RLS z `org`.
