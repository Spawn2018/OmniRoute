# BC named_place_mark (EXP0.6)

HITL katalog znacznika miejsca nazwanego per tenant. mark_code + named_place
+ terms_version 2020|2010 + source_ref. Nie cytat ICC. Nie mutacja wyceny.

## Dozwolone zależności
- `app.models.named_place_mark`
- `app.repositories.named_place_marks`
- `app.domain`

## Zakaz
- import innych BC services (quotations, tenders, charges, extraction)
- zapis `quotation` / `tender` / `charge` / `extraction_draft`
- cytat ICC / 409 DAP na shipment / live ICC API
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
