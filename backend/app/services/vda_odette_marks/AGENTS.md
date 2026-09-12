# BC vda_odette_mark (EXP3.2)

HITL katalog znacznika VDA/Odette per tenant. mark_code + edi_kind
vda|odette|label|other + source_ref. Nie live EDI VDA. Nie etykieta ZPL.

## Dozwolone zaleznosci
- `app.models.vda_odette_mark`
- `app.repositories.vda_odette_marks`
- `app.domain`

## Zakaz
- import innych BC services (edi_messages, edi_map_marks, charges, extraction)
- zapis `edi_message` / `edi_map_mark` / `charge`
- live EDI VDA · Odette HTTP · ZPL / bajty
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
