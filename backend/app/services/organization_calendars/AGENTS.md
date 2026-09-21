# BC organization_calendar (U4)

Katalog dni roboczych i świąt per tenant. `is_working_day` i `fx_rate_day`
liczy Postgres. Offset −1 = poprzedni dzień roboczy (NBP D-1).
Nie GPS. Nie V5. Nie +3 kalendarzowe. Nie mnożenie kursem.

## Dozwolone zależności
- `app.models.organization_calendar`
- `app.repositories.organization_calendars`
- `app.domain`

## Zakaz
- import innych BC services (parties, shipments, charges, nbp_rates)
- zapis `party` / `shipment` / `charge` / `nbp_rate`
- kwoty / marża / float / weekday() w Pythonie
- HTTP / seed świąt PL w kodzie
