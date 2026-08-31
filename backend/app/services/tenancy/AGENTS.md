# BC Tenancy (M-01)

Moduł wzorcowy Golden Standard — RLS + test izolacji.

## Dozwolone zależności
- `app.models`, `app.repositories.tenancy`, `app.core`

## Komendy
- `just migrate` — migracja tenancy
- `pytest backend/tests/tenancy -m integration`

## HC
- Każda nowa tabela biznesowa kopiuje wzorzec RLS z plaster 0.3
- Zero cross-tenant SQL
