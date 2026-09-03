# M-51 drobnica morska — tablica `port` z `is_seaport`

**Moduł żywy:** M-51 (token UI `ocean_lcl`, nie tabela) + M-05 `port`  
**Plaster:** **44.0** (zamknięty) · **111.0** (S49 plan)  
**Status:** operator widzi porty z `is_seaport` i zapisuje odcinek `ocean_lcl` na zleceniu. Nie tabela LCL. Nie CFS.

Delta 44.0: [docs/deltas/archived/44.0-ocean-lcl.md](../deltas/archived/44.0-ocean-lcl.md).  
Delta 111.0: [docs/deltas/open/111.0-shipment-leg-ocean-lcl.md](../deltas/open/111.0-shipment-leg-ocean-lcl.md).

## 44.0 tablica odczytu na `/lcl`

### Zakres

- Ekran `/lcl`: `oceanLclPorts` zostawia wiersze z `is_seaport`
- Link do `/ports`
- Zero nowej tabeli

### Poza 44.0

Tabela LCL · CFS · CBM · live HTTP konsolidatora

### HC

- Marża zostaje w `charge`.
- LLM nie liczy CBM ani stawki.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje geography

## 111.0 odcinek drobnicy na `/lcl`

### Zakres

- Ta sama `shipment_leg`, `leg_kind = ocean_lcl`
- Końce: lokalizacja `unlocode` portu z `is_seaport`
- Jeden odcinek `ocean_lcl` na zlecenie

### Poza 111.0

S50 · CFS · LCL vs FCL · CBM · mapa · HTTP
