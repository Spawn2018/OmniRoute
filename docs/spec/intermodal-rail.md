# M-49 kolej intermodalna — tablica `port` z flagą `rail`

**Moduł żywy:** M-49 (token UI `intermodal_rail`, nie tabela) + M-05 `port`  
**Plaster:** **42.0** (do `/plaster`)  
**Status:** operator **widzi** porty z funkcją kolejową. Nie tabela wagonów. Nie CIM.

Delta: [docs/deltas/open/42.0-intermodal-rail.md](../deltas/open/42.0-intermodal-rail.md).

## 42.0 tablica odczytu na `/rail`

### Zakres

- Ekran `/rail`: `railPorts` zostawia wiersze z `function_flags` zawierającym `rail`
- Link do `/ports`
- Zero nowej tabeli

### Poza 42.0

Wagon · CIM · GPS · rozkład

### HC

- Marża zostaje w `charge`.
- LLM nie liczy trasy.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje geography
