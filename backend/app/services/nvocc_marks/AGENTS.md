# BC nvocc_mark (EXP4.7)

HITL katalog znacznika NVOCC per tenant. mark_code + nvocc_kind
nvocc|house|master|other + source_ref. Nie nvocc live API. Nie scrape.

## Dozwolone zaleznosci
- `app.models.nvocc_mark`
- `app.repositories.nvocc_marks`
- `app.domain`

## Zakaz
- import innych BC services (containers, charges, extraction)
- zapis `container` / `charge` / `extraction_draft`
- nvocc live API · nvocc scrape · kwota
- HTTP
- UPDATE / DELETE wiersza
