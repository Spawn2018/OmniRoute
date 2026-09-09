# BC tower_impact (V6)

HITL katalog etapu łańcucha per tenant. chain_stage + contract_data_status. Nie EBITDA. Nie scoring.

## Dozwolone zależności
- `app.models.tower_impact`
- `app.repositories.tower_impacts`
- `app.domain`

## Zakaz
- import innych BC services (charges, parties, extraction, watchtower)
- zapis `charge` / `party` / `sla_clause` / `party_scorecard`
- kwota / marża / float / EBITDA / scoring osoby
- HTTP / CI5 kara
