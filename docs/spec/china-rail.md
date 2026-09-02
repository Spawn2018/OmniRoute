# M-50 kolej z Chin — tablica `port` CN z flagą `rail`

**Moduł żywy:** M-50 (token UI `china_rail`, nie tabela) + M-05 `port`  
**Plaster:** **43.0** (do `/plaster`)  
**Status:** operator **widzi** chińskie porty kolejowe. Nie tabela korytarza. Nie HTTP.

Delta: [docs/deltas/open/43.0-china-rail.md](../deltas/open/43.0-china-rail.md).

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
