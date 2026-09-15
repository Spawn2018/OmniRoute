# BC article50_mark (AI9.0)

HITL katalog etykiety art. 50 per tenant. mark_code + label_kind
generated|exempt|human|other + source_ref. Nie U-art50 UI. Nie scoring.

## Dozwolone zależności
- `app.models.article50_mark`
- `app.repositories.article50_marks`
- `app.domain`

## Zakaz
- import innych BC services (automation_bias_marks, charges, extraction)
- zapis `automation_bias_mark` / `charge` / `extraction_draft`
- U-art50 przebudowa · live LLM label · scoring
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
