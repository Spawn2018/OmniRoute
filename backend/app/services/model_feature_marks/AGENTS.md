# BC model_feature_mark (AI5.1)

HITL katalog etykiety cechy modelu per tenant. mark_code + feature_kind
numeric|categorical|derived|other + source_ref. Nie live train.

## Dozwolone zaleznosci
- `app.models.model_feature_mark`
- `app.repositories.model_feature_marks`
- `app.domain`

## Zakaz
- import innych BC services (data_sources, ingest_gate_marks, charges, extraction)
- zapis `data_source` / `ingest_gate_mark` / `charge` / `extraction_draft`
- live train · feature store SQL · embedding · pgvector · auto-champion
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
