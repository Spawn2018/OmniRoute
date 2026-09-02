# M-38 dokumenty zlecenia — tablica `source_ref` wyceny

**Moduł żywy:** M-38 (token UI `shipment_document`, nie tabela) + ekran M-21 `quotation`  
**Plaster:** **31.0** (zamknięty)  
**Status:** operator **widzi** `source_ref` wycen z kontrahentem jako dokument. Nie PDF. Nie HBL. Nie nowa tabela.

Delta: [docs/deltas/archived/31.0-shipment-document.md](../deltas/archived/31.0-shipment-document.md).

## 31.0 tablica odczytu na `/shipment-documents`

### Zakres

- Ekran `/shipment-documents`: lista wycen z `party_id` (ten sam filtr co 28.0)
- Pokazuje `source_ref` i kwotę przez `<Money/>`. Link do `/shipments` i `/quotations`
- Zero nowej tabeli. Zero PDF. Zero HBL

### Poza 31.0

Tabela dokumentów · HBL / B/L · U-print · EDI (M-39) · letterhead

### HC

- Marża zostaje w `charge`. Tablica nie odejmuje kwot.
- LLM nie pisze treści dokumentu.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje quotations
