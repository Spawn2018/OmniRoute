# weather_observation (V2)

Katalog obserwacji pogody per tenant. HITL warunek + UN/LOCODE + czas ze strefą. Nie Open-Meteo. Nie silnik ETA.

- RLS FORCE. OpenFGA `can_manage_weather_observations` = member
- `condition_code`: `clear` / `rain` / `snow` / `wind` / `fog` / `ice` / `other`
- `station_unlocode`: 5 znaków `^[A-Z]{2}[A-Z0-9]{3}$`, nie resolve geography
- `observed_at`: ISO-8601 ze strefą; naiwny czas → 400
- `provider_code`: tylko `hitl`
- Unique `(organization_id, source_ref)`
- Job: `/weather-observations`

Delta: [195.0](../deltas/archived/195.0-weather-observation.md).
