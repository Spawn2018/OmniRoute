# BC three_way_mark (EXP3.3c)

HITL katalog znacznika 3-way per tenant. mark_code + way_kind
buyer|seller|carrier|other + source_ref. Nie tuple OpenFGA per strona.
Nie wspólny SELECT. Nie kwota. Odrębny od collaboration_mark (CT11).

## Dozwolone zależności
- `app.models.three_way_mark`
- `app.repositories.three_way_marks`
- `app.domain`

## Zakaz
- import innych BC services (collaboration_marks, charges, extraction)
- zapis `collaboration_mark` / `charge` / `extraction_draft`
- tuple OpenFGA per strona / wspólny SELECT cross-shipper
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
