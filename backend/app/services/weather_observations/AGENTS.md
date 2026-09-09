# BC weather_observation (V2)

HITL katalog obserwacji pogody per tenant. condition_code + station_unlocode + observed_at. Nie Open-Meteo. Nie ETA.

## Dozwolone zależności
- `app.models.weather_observation`
- `app.repositories.weather_observations`
- `app.domain`

## Zakaz
- import innych BC services (trips, stops, charges, extraction, geography)
- zapis `trip` / `stop` / `charge` / `prediction_ledger`
- lat/lng / WMO z API / kg / kwota / marża / float
- HTTP / Open-Meteo / IMGW
