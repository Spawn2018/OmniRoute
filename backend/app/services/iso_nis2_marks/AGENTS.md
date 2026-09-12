# BC iso_nis2_mark (EXP2.26)

HITL katalog znacznika ISO/NIS2 ops per tenant. mark_code + ops_kind
iso|nis2|policy|other + source_ref. Nie audyt live. Nie certyfikat HTTP.

## Dozwolone zaleznosci
- `app.models.iso_nis2_mark`
- `app.repositories.iso_nis2_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, extraction, legal_hold_marks)
- zapis `charge` / `extraction_draft` / `legal_hold_mark`
- audyt live · certyfikat HTTP · scoring
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
