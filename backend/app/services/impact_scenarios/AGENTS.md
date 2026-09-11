# BC impact_scenario (CI6)

HITL katalog scenariusza skutku per tenant. scenario_code + chain_label + source_ref. Nie EBITDA. Nie SQL.

## Dozwolone zależności
- `app.models.impact_scenario`
- `app.repositories.impact_scenarios`
- `app.domain`

## Zakaz
- import innych BC services (tower_impacts, charges, remediation_options, extraction)
- zapis `tower_impact` / `charge` / `remediation_option`
- EBITDA SQL / float / marża / scoring osoby
- HTTP
- UPDATE / DELETE wiersza
