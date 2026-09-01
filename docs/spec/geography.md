# M-05 Geografia — port, lokalizacja, strefy, terminal

**Moduł żywy:** M-05 (archiwum M-05; nie koliduje z żywym M-07 `rate_line` / M-08 `charge`)  
**Plastry:** **4.0** `port` (ten spec, do kodu) · **4.1** `location` + strefy · **4.2** `terminal` + WPI  
**Status 4.0:** Plan zaakceptowany. Nie fundament, dopóki gate po `/plaster`.

## 4.0 `port`

### Zakres

- Tabela `port`: `organization_id`, `unlocode` (5 znaków, np. `PLGDY`), `name`, `country_code`, `lat`/`lng` Numeric, `is_seaport`, `function_flags` (port / rail / airport / ICD — model funkcji, nie gem Seacon), `aliases text[]`, `is_official`, `source_ref`, timestamps
- Unikalność `(organization_id, unlocode)`
- `resolve(token)` — `unlocode` albo alias (bez rozróżniania wielkości); nieznany token = odrzut (nie luźny string)
- Seed: `cristan/improved-un-locodes` (pin SHA); rodowód UNECE `datasets/un-locode` w `source_ref`. Upsert poza HTTP, per tenant. Testy = fixture, zero sieci w CI
- OpenFGA `can_manage_geography` = member
- UI `/ports`: DataTableShell + dodanie nieoficjalnego + rozwiązanie tokenu

### Poza 4.0

`location`, `location_zone_member`, `terminal`, WPI, OSM, ISPS, FK do `party`, `quotation` POL/POD, live GitHub na endpoint, alias jako osobna tabela.

### HC

- RLS FORCE + test izolacji
- `organization_id` na każdym wierszu (archiwalny NULL / globalny PK odrzucony)
- LLM nie liczy; współrzędne nie float
- Wywołanie zewnętrzne (ingest) idempotentne; nie w requestcie API

## 4.1 — kolejka (nie ten plaster)

`location` (`unlocode` | `postal_zone` | `address`; **bez** kind `terminal`) + `location_zone_member` (zakresy kodów pocztowych per strefa tenanta) + UI stref taryfowych. Strefy konfigurowalne per organizacja — żaden tenant nie dostaje cudzego podziału.

Start: `/plan-modul` po zamknięciu 4.0. Nie Q2.

## 4.2 — kolejka (nie ten plaster)

`terminal` (kod ISPS na terminalu; operator jako tekst, bez `operator_party_id` aż M-10) + pola World Port Index (NGA) na `port`. OSM geometria **poza M-05**.

Start: `/plan-modul` po 4.1. Potem Q2 M-10.
