# M-05 Geografia — port, lokalizacja, strefy, terminal

**Moduł żywy:** M-05 (archiwum M-05; nie koliduje z żywym M-07 `rate_line` / M-08 `charge`)  
**Plastry:** **4.0** `port` (w kodzie) · **4.1** `location` + strefy (w kodzie) · **4.2** `terminal` + WPI (kolejka)  
**Status:** 4.0 i 4.1 na origin, gate zielony. 4.2 czeka na Plan.

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

## 4.1 `location` + strefy taryfowe

### Zakres

- Tabela `location`: `organization_id`, `kind` (`unlocode` | `postal_zone` | `address`; **bez** kind `terminal`), `name`, `code`, `port_id`, `country_code`, `city`, `address_line`, `postal_code`, `lat`/`lng` Numeric, `source_ref`, timestamps. CHECK kształtu per `kind`; `code` unikalny per tenant, gdy nie NULL
- Strefa taryfowa **nie ma własnej tabeli** — to wiersz `location` z `kind = 'postal_zone'`
- `kind = 'unlocode'` wiąże się z 4.0 przez FK złożone `(organization_id, port_id)` → `port(organization_id, id)`; 4.1 dokłada na `port` brakujący nośnik `uq_port_org_id`
- Tabela `location_zone_member`: zakres `country_code` + `postal_from`/`postal_to` jako znormalizowany tekst. Kraj siedzi na wierszu członkowskim — strefa bywa wielokrajowa
- Nakładanie zakresów jednego tenanta zakazuje **baza**: typ `postal_range` (subtype `text`, kolacja `"C"`), kolumna generowana `postal_span`, `EXCLUDE USING gist (organization_id WITH =, country_code WITH =, postal_span WITH &&)`
- `resolve(country_code, postal_code)` liczy Postgres: `postal_span @> cast(:code as text)` plus `length(postal_from) = length(:code)`. Bez filtru długości `811989` wpada leksykograficznie w `[81000, 81999]`. Brak trafienia = `UnknownPostalZone`, nie `None`
- OpenFGA bez zmian: `can_manage_geography`
- UI `/locations`: DataTableShell + dodanie strefy, panel zakresów, resolve kodu pocztowego

### Poza 4.1

`terminal`, WPI, geometria poligonowa i OSM, strefy czasu dojazdu, ISPS, FK do `party`, POL/POD w `quotation`, podpięcie `rate_line`, `pg_trgm`.

### HC

- RLS FORCE na obu tabelach + test izolacji dwóch organizacji
- `organization_id` na każdym wierszu; `organization_id WITH =` także w exclusion, bo ten patrzy poza RLS
- Kolacja `"C"` jest warunkiem poprawności, nie stylem — domyślna kolacja PL/DE sortuje inaczej niż bajtowo
- Wymóg `kind = 'postal_zone'` dla `zone_location_id` egzekwuje serwis; CHECK nie sięga innej tabeli
- `source_ref` obowiązkowy; strefy tenanta = `tenant:manual`

## 4.2 — kolejka (nie ten plaster)

`terminal` (kod ISPS na terminalu; operator jako tekst, bez `operator_party_id` aż M-10) + pola World Port Index (NGA) na `port`. OSM geometria **poza M-05**.

Start: `/plan-modul` po 4.1. Potem Q2 M-10.
