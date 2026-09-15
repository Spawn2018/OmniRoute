# BC cfo_narrative_mark (AI7.1)

HITL katalog etykiety narracji CFO per tenant. mark_code + narrative_kind
anomaly|story|summary|other + source_ref. Nie silnik narracji.

## Dozwolone zaleznosci
- `app.models.cfo_narrative_mark`
- `app.repositories.cfo_narrative_marks`
- `app.domain`

## Zakaz
- import innych BC services (allocation_keys, cost_category_marks, charges, extraction)
- zapis `allocation_key` / `cost_category_mark` / `charge` / `extraction_draft`
- silnik narracji · druga marza · SQL TCM · EBITDA z modelu
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
