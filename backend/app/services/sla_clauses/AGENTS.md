# BC sla_clause (CI1)

HITL klauzula SLA per tenant. clause_code + metric_kind + threshold_label + FK customer_contract + source_ref. Nie extract. Nie kara SQL. Nie ciphertext.

## Dozwolone zależności
- `app.models.sla_clause`
- `app.models.customer_contract` — odczyt nagłówka, nie zapis
- `app.repositories.sla_clauses`
- `app.domain`

## Zakaz
- import innych BC services (customer_contracts, charges, extraction, tower_impacts)
- zapis `customer_contract` / `charge` / `extraction_draft`
- extract LLM / upload PDF / penalty_ciphertext / obligation_ciphertext
- kwota / marża / float / kara SQL
- HTTP
- UPDATE / DELETE wiersza
