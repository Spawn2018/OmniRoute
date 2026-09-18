# BC waste_mark (C6)

HITL katalog znacznika odpadów per tenant. mark_code + waste_kind
bdo|kpo|wsr|other + source_ref. Nie MOS live. Nie shipment.is_waste.

## Dozwolone zależności
- `app.models.waste_mark`
- `app.repositories.waste_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipments, filing_scheme_marks, charges, extraction)
- zapis `shipment` / `relation_document_requirement` / `charge`
- MOS / BDO HTTP / kolumna is_waste
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
