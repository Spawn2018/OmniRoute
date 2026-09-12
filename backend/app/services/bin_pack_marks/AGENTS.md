# BC bin_pack_mark (EXP2.16)

HITL katalog znacznika bin-pack per tenant. mark_code + pack_kind
volume|weight|mixed|other + source_ref. Nie solver OR. Nie LLM-VRP.
Obok `load_plan_mark` (G6) — tu bin-pack, nie osie/tunel ADR.

## Dozwolone zależności
- `app.models.bin_pack_mark`
- `app.repositories.bin_pack_marks`
- `app.domain`

## Zakaz
- import innych BC services (load_plan_marks, charges, extraction, trips)
- zapis `load_plan_mark` / `charge` / `shipment` / `extraction_draft`
- solver OR / LLM-VRP / OR-Tools / wymiary Decimal
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
