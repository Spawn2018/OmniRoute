# BC compliance_program_mark (AI9.2 leftover)

HITL katalog stancji programu zgodności per tenant. mark_code +
program_kind draft|review|signed|exempt|other + source_ref.
Nie bajty PDF. Nie U-art50 przebudowa.

## Dozwolone zależności
- `app.models.compliance_program_mark`
- `app.repositories.compliance_program_marks`
- `app.domain`

## Zakaz
- import innych BC services (risk_register_marks, extraction, charges)
- zapis `risk_register_mark` / `extraction_draft` / `charge`
- bajty PDF · U-art50 przebudowa · L3 write · scoring osoby
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
