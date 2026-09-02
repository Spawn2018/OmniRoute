# M-35 zlecenie — tablica wycen z kontrahentem

**Moduł żywy:** M-35 (token UI `shipment`, nie tabela) + ekran M-21 `quotation`  
**Plaster:** **28.0** (plan)  
**Status:** operator **widzi** wyceny z `party_id` jako pracę handlową do zlecenia. Nie nowa tabela. Nie tracking.

Delta: [docs/deltas/open/28.0-shipment.md](../deltas/open/28.0-shipment.md).

## 28.0 tablica odczytu na `/shipments`

### Zakres

- Ekran `/shipments`: lista wycen z `party_id` (ten sam filtr co 22.0)
- Kwota przez `<Money/>`. Link do `/quotations`
- Zero nowej tabeli. Zero `shipment_leg`. Zero HBL / kontenerów

### Poza 28.0

Tabela `shipment` · odcinki · tracking (M-36) · wyjątki (M-37) · dokumenty zlecenia (M-38) · EDI · druga marża

### HC

- Marża zostaje w `charge`. Tablica nie odejmuje kwot.
- LLM nie liczy i nie nadaje numeru zlecenia.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje quotations
