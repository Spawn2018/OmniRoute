# BC automation_bias_mark (AI9.1)

HITL katalog mitygacji automation bias per tenant. mark_code +
bias_kind confirm|delay|review|other + source_ref. Nie ui-04 przebudowa. Nie scoring. Nie auto-accept.

## Dozwolone zależności
- `app.models.automation_bias_mark`
- `app.repositories.automation_bias_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, extraction, risk_register_marks)
- zapis `charge` / `extraction_draft` / `risk_register_mark`
- ui-04 przebudowa · scoring · auto-accept · L3
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
