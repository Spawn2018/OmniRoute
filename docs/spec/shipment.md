# M-35 zlecenie — tabela `shipment` z wyceny

**Moduł żywy:** M-35 (token `shipment`)  
**Plaster:** **90.0** (S28; 28.0 był tablicą wycen)  
**Status:** operator **zapisuje** zlecenie z wyceny z `party_id`. Nie tracking. Nie kwota na wierszu.

Delta: [docs/deltas/archived/90.0-shipment-table.md](../deltas/archived/90.0-shipment-table.md).

## 90.0 tabela na `/shipments`

### Zakres

- Tabela `shipment`: RLS FORCE, FK tenanta do `quotation` i `party`, jeden wiersz na wycenę
- `GET/POST /shipments`, OpenFGA `can_manage_shipments`
- Ekran `/shipments`: lista tabeli + „Zapisz zlecenie”. `data-shipment="board"`

### Poza 90.0

Odcinki · tracking (M-36) · wyjątki (M-37) · dokumenty (M-38) · EDI · auto z S11 · bramka sankcji · druga marża · QR/PDF (D9d)

## 204.0 `shipment_ref` HITL

Opcjonalny twardy numer na `shipment`. Unique per tenant gdy nie NULL. `fixture://shipment-ref/…` albo `omni://shipment/` + token. Nie QR. Nie PDF. Nie 409 wyjazdu. Nie generator GD.

Delta: [docs/deltas/archived/204.0-shipment-ref.md](../deltas/archived/204.0-shipment-ref.md).

### HC

- Marża zostaje w `charge`. Zlecenie nie niesie kwoty.
- LLM nie liczy i nie nadaje numeru zlecenia.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje `shipment` ani quotations
