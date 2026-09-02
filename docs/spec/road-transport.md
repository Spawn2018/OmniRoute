# M-48 transport drogowy — tablica `location` lądowa

**Moduł żywy:** M-48 (token UI `road_transport`, nie tabela) + M-05 `location`  
**Plaster:** **41.0** (do `/plaster`)  
**Status:** operator **widzi** strefy pocztowe i adresy. Nie tabela TMS. Nie GPS.

Delta: [docs/deltas/open/41.0-road-transport.md](../deltas/open/41.0-road-transport.md).

## 41.0 tablica odczytu na `/road`

### Zakres

- Ekran `/road`: `roadLocations` zostawia `kind` `postal_zone` i `address`
- Link do `/locations`
- Zero nowej tabeli. Zero `unlocode` na tej tablicy

### Poza 41.0

TMS · naczepa · GPS · live ETA

### HC

- Marża zostaje w `charge`.
- LLM nie liczy trasy.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje geography
