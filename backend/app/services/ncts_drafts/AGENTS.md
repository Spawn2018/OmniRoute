# BC ncts_draft (G4)

HITL katalog szkicu NCTS per tenant. draft_code + transit_kind t1|t2|other + source_ref. Nie PUESC. Nie kwota.

## Dozwolone zależności
- `app.models.ncts_draft`
- `app.repositories.ncts_drafts`
- `app.domain`

## Zakaz
- import innych BC services (monitoring_schemes, charges, extraction, geography)
- zapis `monitoring_scheme` / `charge` / `shipment` / `stop`
- PUESC HTTP / XML / plomba z nóg / amount / float / kwota
- HTTP
- UPDATE / DELETE wiersza
