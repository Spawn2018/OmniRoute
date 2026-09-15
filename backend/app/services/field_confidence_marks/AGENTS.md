# BC field_confidence_mark (AI9.1 leftover)

HITL katalog pasma pewności per pole per tenant. mark_code +
band_kind green|yellow|orange|hold|other + source_ref.
Nie przebudowa ui-04. Nie float auto-accept.

## Dozwolone zależności
- `app.models.field_confidence_mark`
- `app.repositories.field_confidence_marks`
- `app.domain`

## Zakaz
- import innych BC services (automation_bias_marks, extraction, charges)
- zapis `automation_bias_mark` / `extraction_draft` / `charge`
- przebudowa ui-04 · float confidence · auto-accept · scoring osoby
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
