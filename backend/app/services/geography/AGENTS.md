# BC geography (M-05)

Katalog portów per tenant: UN/LOCODE, aliasy na wierszu, `resolve` tokenu.
Nieznany token = odrzut, nie luźna nazwa miejscowości.

## Dozwolone zależności
- `app.models.port`
- `app.repositories.geography`
- `app.domain`

## Zakaz
- import innych BC services
- sieć w warstwie serwisu — ingest dostaje gotowe rekordy, źródło pobiera `scripts/seed_ports.py`
- `location`, `terminal`, World Port Index (4.1 / 4.2)
- float na współrzędnych
