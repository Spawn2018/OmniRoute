# M-49 kolej intermodalna — tablica `port` z flagą `rail`

**Moduł żywy:** M-49 (token UI `intermodal_rail`, nie tabela) + M-05 `port`  
**Plaster:** **42.0** (zamknięty) · **109.0** (zamknięty)  
**Status:** operator widzi porty z flagą `rail` i zapisuje odcinek kolejowy na zleceniu. Nie wagon. Nie CIM. Nie mapa.

Delta 42.0: [docs/deltas/archived/42.0-intermodal-rail.md](../deltas/archived/42.0-intermodal-rail.md).  
Delta 109.0: [docs/deltas/archived/109.0-shipment-leg-rail.md](../deltas/archived/109.0-shipment-leg-rail.md).

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

## 109.0 odcinek kolejowy na `/rail`

### Zakres

- Ta sama `shipment_leg`, `leg_kind = rail`
- Końce: lokalizacja `unlocode` portu z flagą `rail`
- Jeden odcinek `rail` na zlecenie

### Poza 109.0

S48–S49 · mapa · GPS · wagon · CIM
