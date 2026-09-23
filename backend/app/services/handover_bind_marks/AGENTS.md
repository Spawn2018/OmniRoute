# BC handover_bind_mark (N11 leftover 543)

HITL katalog stance wiązania przekazania per tenant. mark_code +
bind_kind note|board|shift|other + source_ref. Nie FK UUID. Nie T6 live.

## Dozwolone zależności
- `app.models.handover_bind_mark`
- `app.repositories.handover_bind_marks`
- `app.domain`

## Zakaz
- import innych BC services (handover_notes, handover_sbar_marks, trips, charges, extraction)
- zapis `handover_note` / `handover_sbar_mark` / `trip` / `charge` / `extraction_draft`
- FK UUID / T6 live / N8 / auto SBAR
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `handover_note` / `trip` / `shipment`
