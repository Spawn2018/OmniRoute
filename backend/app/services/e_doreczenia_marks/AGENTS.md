# BC e_doreczenia_mark (EXP2.19)

HITL katalog znacznika e-Doręczenia per tenant. mark_code + delivery_kind
edoreczenia|receipt|other + source_ref. Nie live e-Doręczenia. Nie ADE HTTP.

## Dozwolone zależności
- `app.models.e_doreczenia_mark`
- `app.repositories.e_doreczenia_marks`
- `app.domain`

## Zakaz
- import innych BC services (e_delivery_marks, mail_drafts, charges, extraction)
- zapis `e_delivery_mark` / `mail_draft` / `charge` / `extraction_draft`
- live e-Doręczenia / ADE HTTP / bajty PDF / amount
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
