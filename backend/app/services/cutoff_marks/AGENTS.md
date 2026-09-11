# BC cutoff_mark (EXP2.8)

HITL katalog rozdzielonego cutoffu per tenant. mark_code + cutoff_kind
booking|document|gate|other + source_ref. Nie silnik cutoff. Nie ETA.

## Dozwolone zależności
- `app.models.cutoff_mark`
- `app.repositories.cutoff_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipments, trips, charges, extraction)
- zapis `shipment` / `trip` / `charge` / `extraction_draft`
- live cutoff engine / ETA SQL / countdown
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
