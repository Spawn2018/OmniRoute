# BC kpi_definition_mark (AI5.0 leftover)

HITL katalog definicji KPI per tenant. mark_code + kpi_kind
otd|otif|custom|other + source_ref. Nie wzór KPI. Nie OTIF%.

## Dozwolone zaleznosci
- `app.models.kpi_definition_mark`
- `app.repositories.kpi_definition_marks`
- `app.domain`

## Zakaz
- import innych BC services (otif_marks, job_metric_marks, cfo_narrative_marks, charges, extraction)
- zapis `otif_mark` / `job_metric_mark` / `charge` / `extraction_draft`
- wzór KPI · OTIF% SQL · live scoring · OMNI READINESS
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
