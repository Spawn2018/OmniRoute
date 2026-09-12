# BC funnel_mark (EXP4.14)

HITL katalog znacznika X7 lejek per tenant. mark_code + funnel_kind
lead|quote|win|other + source_ref. Nie funnel live. Nie CRM attribution.

## Dozwolone zaleznosci
- `app.models.funnel_mark`
- `app.repositories.funnel_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, charges, extraction)
- zapis `trip` / `charge` / `extraction_draft`
- funnel live API · CRM attribution · kwota
- HTTP
- UPDATE / DELETE wiersza
