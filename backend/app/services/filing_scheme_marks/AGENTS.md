# BC filing_scheme_mark (G12)

HITL katalog schematu składania per tenant. mark_code + scheme_kind ics2|cbam|eudr|efti|other + source_ref. Nie SENT-UE. Nie filer live.

## Dozwolone zależności
- `app.models.filing_scheme_mark`
- `app.repositories.filing_scheme_marks`
- `app.domain`

## Zakaz
- import innych BC services (monitoring_schemes, carbon_methods, charges, extraction)
- zapis `monitoring_scheme` / `carbon_method` / `charge` / `operator_notice`
- SENT-UE / filer live / deadline SQL / amount / sent / float / kwota
- HTTP
- UPDATE / DELETE wiersza
