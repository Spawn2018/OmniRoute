# BC ingest_gate_mark (AI5.0 leftover)

HITL katalog bramy ingest per tenant. mark_code + gate_kind
truth|owner|exception|other + source_ref. Nie live ingest.

## Dozwolone zaleznosci
- `app.models.ingest_gate_mark`
- `app.repositories.ingest_gate_marks`
- `app.domain`

## Zakaz
- import innych BC services (data_sources, charges, extraction)
- zapis `data_source` / `charge` / `extraction_draft`
- live ingest · HTTP · api_key · base_url
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
