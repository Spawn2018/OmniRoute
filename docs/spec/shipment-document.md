# M-38 dokumenty zlecenia — wskazanie na zleceniu

**Moduł żywy:** M-38 (token UI `shipment_document`, tabela `shipment_document`)  
**Plaster:** **92.0** (S30; 31.0 był tablicą `source_ref` wyceny)  
**Status:** operator **zapisuje** wskazanie dokumentu na `shipment`. Nie bajty. Nie PDF. Nie HBL.

Delta: [docs/deltas/archived/92.0-shipment-document.md](../deltas/archived/92.0-shipment-document.md).

## 92.0 tabela na `/shipment-documents`

### Zakres

- Tabela `shipment_document`: RLS FORCE, FK tenanta do `shipment`
- `GET/POST /shipment-documents`, OpenFGA `can_manage_shipment_documents`
- Ekran `/shipment-documents`: lista wierszy + „Zapisz dokument”. `data-shipment-document="board"`

### Poza 92.0

HBL / B/L · bajty / upload · U-print · skan M-20 · wyjątki (M-37) · EDI

### HC

- Marża zostaje w `charge`. Dokument nie niesie kwoty.
- LLM nie pisze treści dokumentu.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje dokumentów zlecenia ani quotations
