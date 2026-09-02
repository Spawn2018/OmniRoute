# M-24 ryzyko oferty — odczyt recenzji i karty przy `quotation`

**Moduł żywy:** M-24 (token UI `offer_risk`, nie tabela) + ekran M-21 `quotation`  
**Plaster:** **17.0** (zamknięty)  
**Status:** wycena **czyta** `credit_review` i `party_scorecard` kontrahenta z wiersza. Nie scoring. Nie nowa tabela.

Delta: [docs/deltas/archived/17.0-offer-risk.md](../deltas/archived/17.0-offer-risk.md).

## 17.0 fakty ryzyka przy ofercie

### Zakres

- Na `/quotations`: panel „Ryzyko kontrahenta oferty” — `party_id` z listy wycen
- `resolveCreditReview(party_id, on_date)` + `fetchPartyScorecard(party_id)`
- Pokazuje `decision` recenzji i snapshot karty (`source_ref`, `computed_at`) — bez nowej liczby
- Zero nowej tabeli. Zero importu parties/scorecards z `quotations` service

### Poza 17.0

Scoring / rating / AI Act · zapis `credit_limit` · nowa tabela `offer_risk` · LLM liczący ryzyko · ExtractionService

### HC

- LLM nie liczy. `charge` zostaje prawdą o marży.
- Recenzja i karta zostają w swoich BC (14.0 / 10.0).
- ExtractionService nie importuje parties / quotations
