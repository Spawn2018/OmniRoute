# BC delay_forecast (CI4)

HITL katalog prognozy opóźnienia per tenant. forecast_code + horizon_hours + p_late Decimal + source_ref. Nie wróżba. Nie GPS.

## Dozwolone zależności
- `app.models.delay_forecast`
- `app.repositories.delay_forecasts`
- `app.domain`

## Zakaz
- import innych BC services (trips, stops, charges, extraction, prediction_ledgers)
- zapis `trip` / `stop` / `charge` / `prediction_ledger`
- wróżba punktowa / GPS / AIS / kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
