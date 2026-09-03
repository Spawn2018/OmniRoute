# M-13 party_scorecard — karta wyników kontrahenta

**Moduł żywy:** M-13 (archiwum M-13; nie koliduje z żywym M-10 `party` / M-08 `charge` / M-14)  
**Plaster:** **10.0** (zamknięty) · **120.0** (S27b plan)  
**Status:** snapshot karty per tenant + odczyt decyzji oferty. Nie silnik RFQ. Nie scoring osoby.

Delta: [docs/deltas/archived/10.0-party-scorecard.md](../deltas/archived/10.0-party-scorecard.md) · [docs/deltas/open/120.0-scorecard-offer-outcomes.md](../deltas/open/120.0-scorecard-offer-outcomes.md).

## 10.0 snapshot karty

### Zakres

- Tabela `party_scorecard` per tenant: `organization_id`, `party_id`, wskaźniki Decimal (`response_rate`, `median_response_hours`, `price_position`, `quote_invoice_match_rate`), `rollover_count`, `sample_size`, `window_days`, `computed_at`, `source_ref`, timestamps
- Unikat `(organization_id, party_id)`. FK złożone do `party`
- Lista rankingowa; GET po `party_id`; upsert ręczny
- OpenFGA `can_manage_parties` = member
- UI `/party-scorecards` + panel na `/parties`

### Poza 10.0

SQL-refresh z `quotation`/`charge` · karta per lane · M-14 `natural_person` / JDG · M-30 RFQ · M-40 faktura vs oferta · `network_member` · ExtractionService · LLM liczący wskaźniki · zmiana `credit_limit` / `charge`

### HC

- RLS FORCE + test izolacji
- Wskaźniki = `Numeric`, nie float; LLM nie liczy
- Marża zostaje w `charge.margin()`
- ExtractionService nie importuje `parties`

## 120.0 decyzje oferty na karcie

### Zakres

- `/party-scorecards` czyta decyzje S11 na wycenie (przyjęta / odrzucona)
- Zero zapisu KPI. Zero nowej tabeli.

### Poza 120.0

SQL-refresh zapisujący wskaźniki · scoring osoby · `won`/`lost` na wycenie
