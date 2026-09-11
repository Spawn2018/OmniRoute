# BC clause_notice (CI3)

HITL katalog powiadomienia o klauzuli per tenant. notice_code + clause_label + source_ref. Nie 409. Nie auto-kara.

## Dozwolone zależności
- `app.models.clause_notice`
- `app.repositories.clause_notices`
- `app.domain`

## Zakaz
- import innych BC services (sla_clauses, charges, operator_notices, extraction)
- zapis `sla_clause` / `charge` / `operator_notice`
- HTTP 409 / auto-kara / float / marża / scoring osoby
- HTTP
- UPDATE / DELETE wiersza
- FK do `sla_clause`
