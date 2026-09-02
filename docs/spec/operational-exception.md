# M-37 wyjątki — tablica niepełnego lane wyceny

**Moduł żywy:** M-37 (token UI `operational_exception`, nie tabela) + ekran M-21 `quotation`  
**Plaster:** **30.0** (zamknięty)  
**Status:** operator **widzi** wyceny z kontrahentem bez pełnego POL/POD. Nie AIS. Nie mapa. Nie nowa tabela.

Delta: [docs/deltas/archived/30.0-operational-exception.md](../deltas/archived/30.0-operational-exception.md).

## 30.0 tablica odczytu na `/exceptions`

### Zakres

- Ekran `/exceptions`: lista wycen z `party_id`, którym brakuje `origin_port_id` albo `destination_port_id`
- Helper `quotationOperationalExceptions` (dopełnienie `quotationLanes`). Link do `/shipments`, `/tracking` i `/quotations`
- Zero nowej tabeli. Zero mapy. Zero ETA

### Poza 30.0

Tabela wyjątków · `shipment_leg` · AIS / project44 · Watchtower mapa · dokumenty zlecenia (M-38) · EDI

### HC

- Marża zostaje w `charge`. Tablica nie liczy opóźnień.
- LLM nie klasyfikuje wyjątku.
- HITL zostaje na ekstrakcji (27.0).
- ExtractionService nie importuje quotations
- `party_charge_override` nie jest tym ekranem
- Mapa nie wchodzi do initial JS (ADR-0003)
