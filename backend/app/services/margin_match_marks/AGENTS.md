# BC margin_match_mark (N6 leftover matching)

HITL katalog stance dopasowania podłogi per tenant. mark_code +
match_kind match|hold|waive|other + source_ref.
Nie matching SQL lane. Nie druga marza.

## Dozwolone zaleznosci
- `app.models.margin_match_mark`
- `app.repositories.margin_match_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, charges, extraction)
- zapis `trip` / `charge` / `extraction_draft`
- SQL wariancji na charge / hold-from-charge / druga marza
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `trip` / `charge` / `shipment`
