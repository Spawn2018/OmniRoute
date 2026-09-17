# BC handover_note (N11 leftover)

HITL wpis przekazania zmiany per tenant. note_code + situation /
background / assessment / recommendation + source_ref. Nie auto SBAR. Nie T6.

## Dozwolone zależności
- `app.models.handover_note`
- `app.repositories.handover_notes`
- `app.domain`

## Zakaz
- import innych BC services (handover_sbar_marks, ops_room_marks, trips, charges)
- zapis `handover_sbar_mark` / `ops_room_mark` / `trip` / `charge`
- auto SBAR z LLM · drugi czat · N8 · FK trip/shipment/mark
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
