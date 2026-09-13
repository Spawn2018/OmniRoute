# BC oog_permit_mark (BR4.1)

HITL katalog znacznika zezwolenia/pilotażu OOG per tenant. mark_code +
permit_kind permit|pilot|route|other + source_ref. Nie wymiary Decimal.
Nie live urząd. Nie oog_mark.

## Dozwolone zaleznosci
- `app.models.oog_permit_mark`
- `app.repositories.oog_permit_marks`
- `app.domain`

## Zakaz
- import innych BC services (oog_marks, trips, shipments, charges, extraction)
- zapis `oog_mark` / `trip` / `shipment` / `charge`
- wymiary Decimal / live zezwolenie / escort party FK
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `oog_mark` / `trip` / `shipment`
