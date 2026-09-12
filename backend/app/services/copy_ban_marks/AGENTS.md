# BC copy_ban_mark (EXP4.19)

HITL katalog znacznika zakazu copy claimów per tenant. mark_code + ban_kind
eight_min|fifteen_k|five_hundred_k|other + source_ref. Nie copy marketingu. Nie silnik.

## Dozwolone zależności
- `app.models.copy_ban_mark`
- `app.repositories.copy_ban_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, extraction, billing_marks)
- zapis `charge` / `extraction_draft` / `billing_mark`
- copy claimów do UI / Bayer scrape / kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
