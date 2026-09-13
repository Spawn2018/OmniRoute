# BC suggestion_kind (AI1.4)

HITL otwarty słownik rodzaju podpowiedzi per tenant. kind_code + source_ref.
Nowy rodzaj = INSERT. Nie CHECK. Nie ENUM. Nie ledger.

## Dozwolone zależności
- `app.models.suggestion_kind`
- `app.repositories.suggestion_kinds`
- `app.domain`

## Zakaz
- import innych BC services (suggestion_ledgers, twin_marks, charges, extraction)
- zapis `suggestion_ledger` / `twin_mark` / `charge` / `extraction_draft`
- CHECK listy rodzajów / ENUM / FK z suggestion_ledger
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
