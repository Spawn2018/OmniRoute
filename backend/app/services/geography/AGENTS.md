# BC geography (M-05)

Katalog portów per tenant: UN/LOCODE, aliasy na wierszu, `resolve` tokenu.
Nieznany token = odrzut, nie luźna nazwa miejscowości.

Lokalizacje i strefy taryfowe per tenant: `location` (`unlocode` | `postal_zone` |
`address`) oraz zakresy kodów pocztowych w `location_zone_member`. Zakres liczy
Postgres — `postal_span` z kolacją "C", nakładanie blokuje exclusion constraint.

## Dozwolone zależności
- `app.models.port`
- `app.models.location`
- `app.repositories.geography`
- `app.domain`

## Zakaz
- import innych BC services
- sieć w warstwie serwisu — ingest dostaje gotowe rekordy, źródło pobiera `scripts/seed_ports.py`
- `terminal`, World Port Index (4.2)
- float na współrzędnych
- walidacja nakładania zakresów w Pythonie — to reguła bazy
