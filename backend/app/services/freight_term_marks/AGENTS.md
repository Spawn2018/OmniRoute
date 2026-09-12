# BC freight_term_mark (EXP1)

HITL katalog znacznika freight term per tenant. mark_code + term_kind
prepaid|collect|third_party|other + source_ref. Nie kolumna shipment. Nie kwota.

## Dozwolone zależności
- `app.models.freight_term_mark`
- `app.repositories.freight_term_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipments, quotations, charges, extraction)
- zapis `shipment` / `quotation` / `charge` / `extraction_draft`
- kolumna freight_term na shipment / auto z Incoterms
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
