# BC bid_decision_mark (EXP1)

HITL katalog znacznika bid decision per tenant. mark_code + decision_kind
go|no_go|hold|other + source_ref. Nie kolumna na quotation. Nie auto-award.

## Dozwolone zależności
- `app.models.bid_decision_mark`
- `app.repositories.bid_decision_marks`
- `app.domain`

## Zakaz
- import innych BC services (quotations, charges, extraction)
- zapis `quotation` / `charge` / `extraction_draft`
- kolumna bid_decision / auto-award / scoring oferty
- kwota / marża / float / score
- HTTP
- UPDATE / DELETE wiersza
