# BC sid_import_mark (EXP2.21)

HITL katalog znacznika importu SID per tenant. mark_code + sid_kind
sid|batch|manual|other + source_ref. Nie SID HTTP. Nie ICS2 live.
Obok `edi_message` — tu znacznik importu, nie parser EDI.

## Dozwolone zależności
- `app.models.sid_import_mark`
- `app.repositories.sid_import_marks`
- `app.domain`

## Zakaz
- import innych BC services (edi_messages, shipments, charges, extraction)
- zapis `edi_message` / `shipment` / `charge` / `extraction_draft`
- SID live · SID HTTP · ICS2 live · bajty
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
