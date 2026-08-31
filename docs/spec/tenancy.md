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

## Sesja JWT (0.12) + hasła (0.15)

- `POST /api/v1/session/token` — `email` + `password` (argon2id); 201: `access_token` + `refresh_token`
- `POST /api/v1/session/refresh` — rotacja; stary refresh → 401
- `GET /api/v1/session/me` — claims z Bearer
- Tożsamość wyłącznie z JWT (`sub`, `org`). OpenFGA = autoryzacja. RLS z `org`.
- Tabela `refresh_token` + RLS. Logowanie: polityka SELECT po `app.login_email` (org jeszcze nieznane).

## Poza zakresem (nadal)
OpenFGA (0.4 — zrobione), UI admin, billing, IdP/OIDC.
