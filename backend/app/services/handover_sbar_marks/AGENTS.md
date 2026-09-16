# BC handover_sbar_mark (N11)

HITL katalog znacznika przekazania zmiany SBAR per tenant. mark_code +
sbar_kind situation|background|assessment|recommendation|other + source_ref.
Nie drugi czat. Nie auto SBAR z T6.

## Dozwolone zależności
- `app.models.handover_sbar_mark`
- `app.repositories.handover_sbar_marks`
- `app.domain`

## Zakaz
- import innych BC services (ops_room_marks, war_room_marks, trips, charges, extraction)
- zapis `ops_room_mark` / `war_room_mark` / `trip` / `charge` / `extraction_draft`
- auto SBAR z LLM · drugi czat · N8 · FK trip/shipment
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
