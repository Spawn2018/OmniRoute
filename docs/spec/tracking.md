# M-36 tracking — zdarzenia na zleceniu

**Moduł żywy:** M-36 (token UI `tracking`, tabela `tracking_event`)  
**Plaster:** **91.0** (S29; 29.0 był tablicą lane)  
**Status:** operator **zapisuje** zdarzenie na `shipment`. Nie AIS. Nie mapa. Nie czas przybycia liczony w kodzie.

Delta: [docs/deltas/archived/91.0-tracking-event.md](../deltas/archived/91.0-tracking-event.md).

## 91.0 tabela na `/tracking`

### Zakres

- Tabela `tracking_event`: RLS FORCE, FK tenanta do `shipment`
- `GET/POST /tracking-events`, OpenFGA `can_manage_tracking`
- Ekran `/tracking`: lista zdarzeń + „Zapisz zdarzenie”. `data-tracking="board"`

### Poza 91.0

`shipment_leg` · AIS · mapa / Watchtower · wyjątki (M-37) · dokumenty (M-38) · czas przybycia liczony

### HC

- Marża zostaje w `charge`. Zdarzenie nie niesie kwoty.
- LLM nie wylicza czasu przybycia.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje trackingu ani quotations
- Mapa nie wchodzi do initial JS (ADR-0003)
