# BC geography (M-05)

Katalog portów per tenant: UN/LOCODE, aliasy na wierszu, `resolve` tokenu.
Nieznany token = odrzut, nie luźna nazwa miejscowości.

Lokalizacje i strefy taryfowe per tenant: `location` (`unlocode` | `postal_zone` |
`address`) oraz zakresy kodów pocztowych w `location_zone_member`. Zakres liczy
Postgres — `postal_span` z kolacją "C", nakładanie blokuje exclusion constraint.

Terminale per tenant: osobna tabela `terminal` (ISPS, `operator_name` tekst,
nullable `operator_party_id` bez importu `app.services.parties`),
`resolve` kodu ISPS. World Port Index to kolumny na `port`, ingest poza HTTP.

## Dozwolone zależności
- `app.models.port`
- `app.models.location`
- `app.models.terminal`
- `app.repositories.geography`
- `app.domain`

## Zakaz
- import innych BC services
- sieć w warstwie serwisu — ingest dostaje gotowe rekordy, źródło pobiera
  `scripts/seed_ports.py` albo `scripts/seed_wpi.py`
- float na współrzędnych i głębokościach
- walidacja nakładania zakresów w Pythonie — to reguła bazy
