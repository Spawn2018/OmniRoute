# M-36 tracking — tablica znanego lane POL/POD

**Moduł żywy:** M-36 (token UI `tracking`, nie tabela) + ekrany M-21 `quotation` i M-05 `port`  
**Plaster:** **29.0** (plan)  
**Status:** operator **widzi** lane wyceny (POL→POD). Nie AIS. Nie mapa. Nie nowa tabela.

Delta: [docs/deltas/open/29.0-tracking.md](../deltas/open/29.0-tracking.md).

## 29.0 tablica odczytu na `/tracking`

### Zakres

- Ekran `/tracking`: lista `quotationLanes` (party + POL + POD)
- UN/LOCODE z katalogu `port`. Link do `/shipments` i `/quotations`
- Zero nowej tabeli. Zero mapy. Zero ETA

### Poza 29.0

Tabela zdarzeń trackingu · `shipment_leg` · AIS / project44 · Watchtower mapa · wyjątki (M-37)

### HC

- Marża zostaje w `charge`. Tablica nie liczy odległości.
- LLM nie wylicza ETA.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje quotations
- Mapa nie wchodzi do initial JS (ADR-0003)
