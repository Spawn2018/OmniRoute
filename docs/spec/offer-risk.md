# M-24 ryzyko oferty — odczyt i wskazanie recenzji przy `quotation`

**Moduł żywy:** M-24 (token `offer_risk`) + ekran M-21 `quotation`  
**Plaster:** **17.0** (odczyt) · **87.0** (wskazanie)  
**Status:** wycena czyta recenzję/kartę i zapisuje `noted_credit_review_id`. Nie scoring.

Delta: [17.0](../deltas/archived/17.0-offer-risk.md) · [87.0](../deltas/archived/87.0-offer-risk-fact.md).

## 17.0 fakty ryzyka przy ofercie

### Zakres

- Panel „Ryzyko kontrahenta oferty” — `resolveCreditReview` + `fetchPartyScorecard`
- Zero importu parties z `quotations` service

## 87.0 wskazanie recenzji

### Zakres

- Kolumna `quotation.noted_credit_review_id`
- `PATCH /quotations/{id}/note-risk` — API składa przez `PartyService.get_review`
- UI „Zapisz fakt”

### Poza 87.0

Scoring · załącznik wywiadowni (S26) · mutacja recenzji · F9.1

## HC

- LLM nie liczy. `charge` zostaje prawdą o marży.
- ExtractionService nie importuje quotations / parties
