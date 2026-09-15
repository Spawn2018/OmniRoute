# BC data_source (AI5.0)

HITL katalog zrodla danych per tenant. source_code + license_label +
rights_scope + source_ref. Nie live ingest. Nie CHECK listy.

## Dozwolone zaleznosci
- `app.models.data_source`
- `app.repositories.data_sources`
- `app.domain`

## Zakaz
- import innych BC services (charges, extraction, twin_kinds)
- zapis `charge` / `extraction_draft` / `twin_kind`
- live ingest · HTTP zewnetrzny · sekrety · api_key · base_url
- CHECK listy licencji · OMNI READINESS · pasek 72%
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
