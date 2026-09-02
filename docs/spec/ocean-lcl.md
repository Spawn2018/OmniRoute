# M-51 drobnica morska — tablica `port` z `is_seaport`

**Moduł żywy:** M-51 (token UI `ocean_lcl`, nie tabela) + M-05 `port`  
**Plaster:** **44.0** (plan)  
**Status:** operator **zobaczy** porty morskie. Nie tabela LCL. Nie CFS.

Delta: [docs/deltas/open/44.0-ocean-lcl.md](../deltas/open/44.0-ocean-lcl.md).

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
