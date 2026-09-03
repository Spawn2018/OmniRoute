# M-48 transport drogowy — tablica `location` lądowa

**Moduł żywy:** M-48 (token UI `road_transport`, nie tabela) + M-05 `location`  
**Plaster:** **41.0** (zamknięty) · **108.0** (S46 plan)  
**Status:** operator widzi strefy pocztowe i zapisuje odcinek drogowy na zleceniu. Nie TMS. Nie GPS. Nie mapa.

Delta 41.0: [docs/deltas/archived/41.0-road-transport.md](../deltas/archived/41.0-road-transport.md).  
Delta 108.0: [docs/deltas/open/108.0-shipment-leg.md](../deltas/open/108.0-shipment-leg.md).

## 41.0 tablica odczytu na `/road`

### Zakres

- Ekran `/road`: `roadLocations` zostawia `kind` `postal_zone` i `address`
- Link do `/locations`
- Zero nowej tabeli. Zero `unlocode` na tej tablicy

### Poza 41.0

TMS · naczepa · GPS · live ETA · odcinek na zleceniu

### HC

- Marża zostaje w `charge`.
- LLM nie liczy trasy.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje geography

## 108.0 odcinek drogowy na `/road`

### Zakres

- Tabela `shipment_leg` (`leg_kind = road`) na tym samym `/road`
- Origin i dest: `postal_zone` albo `address`
- Jeden odcinek `road` na zlecenie

### Poza 108.0

S47–S49 inne kind · mapa · GPS · TMS · flota
