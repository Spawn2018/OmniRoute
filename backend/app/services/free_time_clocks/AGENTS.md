# BC free_time_clock (V3)

HITL katalog zegara D&D per tenant. clock_kind + free_days. Nie countdown. Nie charge.

## Dozwolone zależności
- `app.models.free_time_clock`
- `app.repositories.free_time_clocks`
- `app.domain`

## Zakaz
- import innych BC services (containers, charges, extraction, trips)
- zapis `container` / `charge` / `trip` / `weather_observation`
- countdown / remaining / kwota / marża / float
- HTTP / szkic charge / blank sailing
