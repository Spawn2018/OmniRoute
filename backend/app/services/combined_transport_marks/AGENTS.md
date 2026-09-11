# BC combined_transport_mark (EXP2.12)

HITL katalog reżimu combined transport per tenant. mark_code + regime_kind
combined|mobility|piggyback|other + source_ref. Nie silnik. Nie Mobility Package live.

## Dozwolone zależności
- `app.models.combined_transport_mark`
- `app.repositories.combined_transport_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipments, shipment_legs, charges, extraction)
- zapis `shipment` / `shipment_leg` / `charge` / `extraction_draft`
- combined transport live / Mobility Package silnik / Huckepack solver
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza