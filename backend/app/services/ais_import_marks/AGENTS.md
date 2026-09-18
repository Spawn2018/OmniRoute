# BC ais_import_mark (C2)

HITL katalog znacznika AIS/AES/Intrastat per tenant. mark_code + import_kind
ais|aes|intrastat|other + source_ref. Nie PUESC live. Nie XML.

## Dozwolone zależności
- `app.models.ais_import_mark`
- `app.repositories.ais_import_marks`
- `app.domain`

## Zakaz
- import innych BC services (sid_import_marks, filing_scheme_marks, charges, extraction)
- zapis `sid_import_mark` / `filing_scheme_mark` / `shipment` / `charge`
- PUESC HTTP / AIS XML / AES / Intrastat live
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
