# M-37 wyjątki — zapis na zleceniu

**Moduł żywy:** M-37 (token UI `operational_exception`, tabela `operational_exception`)  
**Plaster:** **93.0** (S31; 30.0 był tablicą wycen bez POL/POD)  
**Status:** operator **zapisuje** wyjątek na `shipment`. Nie AIS. Nie mapa. Nie filtr wycen.

Delta: [docs/deltas/archived/93.0-operational-exception.md](../deltas/archived/93.0-operational-exception.md).

## 93.0 tabela na `/exceptions`

### Zakres

- Tabela `operational_exception`: RLS FORCE, FK tenanta do `shipment`
- `GET/POST /operational-exceptions`, OpenFGA `can_manage_exceptions`
- Ekran `/exceptions`: lista wierszy + „Zapisz wyjątek”. `data-operational-exception="board"`

### Poza 93.0

Watchtower / mapa (S32) · AIS · czas przybycia liczony · `shipment_leg` · `party_charge_override`

### HC

- Marża zostaje w `charge`. Wyjątek nie niesie kwoty.
- LLM nie klasyfikuje wyjątku.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje wyjątków ani quotations
- Mapa nie wchodzi do initial JS (ADR-0003)
