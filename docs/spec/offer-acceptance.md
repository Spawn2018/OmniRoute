# M-29 wykrywanie akceptacji — pending i decyzja S11

**Moduł żywy:** M-29 (token `offer_acceptance`) + szyna M-71 `operator_decision`  
**Plaster:** **22.0** (pending) · **86.0** (zapis decyzji)  
**Status:** operator widzi pending i zapisuje Przyjmij / Odrzuć przez S11. Nie HITL extract. Nie IMAP.

Delta: [22.0](../deltas/archived/22.0-offer-acceptance.md) · [86.0](../deltas/archived/86.0-offer-acceptance-decision.md).

## 22.0 pending z wycen

### Zakres

- Na `/quotations`: panel „Akceptacja oferty” — wiersze z `party_id`, kwota przez `<Money/>`
- Zero nowej tabeli. Zero angielskich etykiet wyniku. Zero endpointu HITL

## 86.0 decyzja na wycenie

### Zakres

- `operator_decision.subject_kind` dopuszcza `quotation`
- Przyjmij / Odrzuć woła istniejące API decyzji
- Przyjęta wycena znika z pending
- Serwis decyzji nie importuje `quotations`

### Poza 86.0

CSV · `changed` · accept extractu · mutacja kwoty · F9.1

## HC

- Kwota zostaje ze `rate_line` (SQL). Panel nic nie liczy.
- HITL accept zostaje przy ekstrakcji, nie przy ofercie.
- LLM nie liczy. `charge` zostaje prawdą o marży.
- ExtractionService nie importuje quotations
