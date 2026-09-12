# BC language_code_mark (EXP1)

HITL katalog kodu języka per tenant. mark_code + locale_kind
pl|en|de|other + source_ref. Nie kolumna shipment. Nie preferred_language party.

## Dozwolone zależności
- `app.models.language_code_mark`
- `app.repositories.language_code_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipments, parties, charges, extraction)
- zapis `shipment` / `party` / `charge` / `extraction_draft`
- kolumna language na shipment / party.preferred_language / i18n UI
- kwota / marża / float / score
- HTTP
- UPDATE / DELETE wiersza
