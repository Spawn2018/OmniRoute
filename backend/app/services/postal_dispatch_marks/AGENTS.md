# BC postal_dispatch_mark (F11)

HITL katalog stancji ksiazki PP per tenant. mark_code +
dispatch_kind en|uss|epo|other + source_ref. Nie live Poczta Polska.
Nie e-Doreczenia.

## Dozwolone zależności
- `app.models.postal_dispatch_mark`
- `app.repositories.postal_dispatch_marks`
- `app.domain`

## Zakaz
- import innych BC services (e_doreczenia_marks, e_delivery_marks, charges, extraction)
- zapis `e_doreczenia_mark` / `e_delivery_mark` / `charge` / `extraction_draft`
- live Poczta Polska / EN / USS / EPO HTTP / bajty listu
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
