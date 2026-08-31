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

## Runtime RLS (0.16 T1)

- Rola `omniroute_app`: `NOSUPERUSER` + `NOBYPASSRLS` (migracja 005)
- `DATABASE_URL` runtime = `omniroute_app`; `DATABASE_URL_SYNC` = owner `omniroute` (Alembic)
- Superuser `omniroute` nie jest rolą aplikacji
- Test atrybutów roli + SELECT bez `app.current_org` → 0 wierszy: integration CI (lokalnie PG może wisieć)

## Matryca RLS S1–S6 (0.17 T2)

Jawne `WITH CHECK` na politykach tenant (nie FOR SELECT). Integration = CI.

| ID | Scenariusz | Dowód |
|---|---|---|
| S1 | SELECT | tenant A nie czyta wierszy B |
| S2 | INSERT | wiersz z `organization_id` B przy kontekście A → odrzut |
| S3 | UPDATE USING | UPDATE wiersza B przy kontekście A → 0 wierszy |
| S4 | UPDATE WITH CHECK | zmiana `organization_id` A→B → odrzut |
| S5 | DELETE | DELETE wiersza B przy kontekście A → 0 wierszy |
| S6 | brak `app.current_org` | SELECT pusty; INSERT odrzut |

## OpenFGA (0.20 A2)

- `can_review_extractions` = `reviewer`, nie `member`
- First-login zapisuje tylko `member`. Reviewer = ręczny seed.

## Poza zakresem (nadal)
UI admin, billing, IdP/OIDC.
