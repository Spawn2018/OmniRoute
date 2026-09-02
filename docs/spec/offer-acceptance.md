# M-29 wykrywanie akceptacji — pending z faktów wyceny

**Moduł żywy:** M-29 (token UI `offer_acceptance`, nie tabela) + ekran M-21 `quotation`  
**Plaster:** **22.0** (zamknięty)  
**Status:** operator **widzi** wyceny wystawione kontrahentowi jako oczekujące na akceptację. Nie zapis wyniku. Nie HITL extract. Nie IMAP.

Delta: [docs/deltas/archived/22.0-offer-acceptance.md](../deltas/archived/22.0-offer-acceptance.md).

## 22.0 pending z wycen

### Zakres

- Na `/quotations`: panel „Akceptacja oferty” — wiersze z `party_id`, kwota przez `<Money/>`
- Brak zapisu w bazie = brak wykrytej akceptacji (nie zgadujemy kolumny statusu)
- Zero nowej tabeli. Zero `won`/`lost`. Zero endpointu HITL

### Poza 22.0

Tabela wyniku · kolumna statusu na `quotation` · IMAP (M-32) · auto-detect z maila · accept HITL (M-20) · LLM

### HC

- Kwota zostaje ze `rate_line` (SQL). Panel nic nie liczy.
- HITL accept zostaje przy ekstrakcji, nie przy ofercie.
- LLM nie liczy. `charge` zostaje prawdą o marży.
- ExtractionService nie importuje quotations
