# BC reefer_mark (EXP4.5)

HITL katalog znacznika reefer per tenant. mark_code + reefer_kind
reefer|setpoint|genset|other + source_ref. Nie reefer live API. Nie scrape.

## Dozwolone zaleznosci
- `app.models.reefer_mark`
- `app.repositories.reefer_marks`
- `app.domain`

## Zakaz
- import innych BC services (containers, charges, extraction)
- zapis `container` / `charge` / `extraction_draft`
- reefer live API · reefer scrape · kwota · setpoint SQL
- HTTP
- UPDATE / DELETE wiersza
