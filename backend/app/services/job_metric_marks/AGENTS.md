# BC job_metric_mark (EXP4.21 / M-72)

HITL katalog znacznika metryki jobu per tenant. mark_code + metric_kind
time_to_fix|touches|rework|other + source_ref. Nie scoring osoby. Nie SQL job.

## Dozwolone zależności
- `app.models.job_metric_mark`
- `app.repositories.job_metric_marks`
- `app.domain`

## Zakaz
- import innych BC services (entity_events, charges, extraction)
- zapis `entity_event` / `charge` / `extraction_draft`
- scoring osoby / SQL job engine / kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
