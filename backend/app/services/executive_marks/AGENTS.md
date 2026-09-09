# BC executive_mark (W4)

HITL katalog rodzaju pytania zarządu per tenant. question_kind. Nie suma LLM. Nie zdania z agregatów SQL.

## Dozwolone zależności
- `app.models.executive_mark`
- `app.repositories.executive_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, quotations, extraction, memory_edges)
- zapis `charge` / `quotation` / `prediction_ledger` / `extraction_draft`
- suma LLM / EBITDA / kwota / marża / float
- HTTP / ranking W5
