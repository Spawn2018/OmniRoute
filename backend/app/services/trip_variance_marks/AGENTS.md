# BC trip_variance_mark (P5 leftover P5b)

HITL katalog stance wariancji przejazdu per tenant. mark_code +
variance_kind expected|actual|gap|other + source_ref.
Nie SQL na charge. Nie druga marza.

## Dozwolone zaleznosci
- `app.models.trip_variance_mark`
- `app.repositories.trip_variance_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, charges, extraction)
- zapis `trip` / `charge` / `extraction_draft`
- SQL wariancji na charge / actual-from-charge / druga marza
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `trip` / `charge` / `shipment`
