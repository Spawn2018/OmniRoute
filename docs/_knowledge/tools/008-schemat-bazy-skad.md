# Tools — skąd schemat bazy

MCP Postgres **nie jest** podłączony (`mcp.json` = GitHub). Kontrakt kazał czytać MCP — to była fikcja. Nie dopinaj serwera z zapisem ani `BYPASSRLS`.

## Skąd brać schemat

1. `backend/alembic/versions/` — najnowsza migracja **tej tabeli**.
2. Modele **tego jednego BC** (`backend/app/models/<bc>`), nie cały pakiet modeli.
3. Żywa baza: operator / test, nie agent z rolą app.

Nie czytaj wszystkich modeli „na zapas”. Nie zgaduj kolumn.

Gdyby kiedyś MCP: osobny plaster fabryki, rola `omniroute_ro`, `NOBYPASSRLS`, `GRANT SELECT` na katalog, connection string z env.
