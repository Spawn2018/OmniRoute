# M-50 kolej z Chin — tablica `port` CN z flagą `rail`

**Moduł żywy:** M-50 (token UI `china_rail`, nie tabela) + M-05 `port`  
**Plaster:** **43.0** (zamknięty) · **110.0** (S48 plan)  
**Status:** operator widzi porty CN z flagą `rail` i zapisuje odcinek `china_rail` na zleceniu. Nie korytarz. Nie HTTP.

Delta 43.0: [docs/deltas/archived/43.0-china-rail.md](../deltas/archived/43.0-china-rail.md).  
Delta 110.0: [docs/deltas/open/110.0-shipment-leg-china-rail.md](../deltas/open/110.0-shipment-leg-china-rail.md).

## 43.0 tablica odczytu na `/china-rail`

### Zakres

- Ekran `/china-rail`: `chinaRailPorts` zostawia `country_code = CN` i flagę `rail`
- Link do `/rail` i `/ports`
- Zero nowej tabeli

### Poza 43.0

Korytarz · rozkład CR · live HTTP

### HC

- Marża zostaje w `charge`.
- LLM nie liczy trasy.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje geography

## 110.0 odcinek kolej z Chin na `/china-rail`

### Zakres

- Ta sama `shipment_leg`, `leg_kind = china_rail`
- Końce: lokalizacja `unlocode` portu z flagą `rail` i `country_code = CN`
- Jeden odcinek `china_rail` na zlecenie

### Poza 110.0

S49 · korytarz · mapa · GPS · HTTP CR
