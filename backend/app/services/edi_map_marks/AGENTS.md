# BC edi_map_mark (G13)

HITL katalog mapy pól EDI per tenant. mark_code + map_kind field_map|segment|other + source_ref. Nie silent write. Nie parser live.

## Dozwolone zależności
- `app.models.edi_map_mark`
- `app.repositories.edi_map_marks`
- `app.domain`

## Zakaz
- import innych BC services (edi_messages, shipments, charges, extraction)
- zapis `edi_message` / `shipment` / `charge` / `extraction_draft`
- silent write / parser live / amount / payload / float / kwota
- HTTP
- UPDATE / DELETE wiersza
