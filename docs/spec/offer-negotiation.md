# M-25 negocjacja i wynik — odczyt `channel_quote` przy `quotation`

**Moduł żywy:** M-25 (token UI `offer_negotiation`, nie tabela) + ekran M-21 `quotation`  
**Plaster:** **18.0** (plan)  
**Status:** plan — wycena **czyta** katalog 13.0 na tej samej lane. Nie zapis wyniku won/lost. Nie odejmowanie kwot.

Delta: [docs/deltas/open/18.0-offer-negotiation.md](../deltas/open/18.0-offer-negotiation.md).

## 18.0 oferta kanału przy wycenie

### Zakres

- Na `/quotations`: panel „Oferta kanału przy wycenie” — wiersz z `party_id` + POL + POD
- `resolveChannelQuote` (armator, POL, POD, dzień)
- Pokazuje kwotę kanału i kwotę wyceny osobno (`<Money/>`) — bez różnicy w JS
- Zero nowej tabeli. Zero importu `channel_quotes` z `quotations` service

### Poza 18.0

Katalog `won`/`lost` · mutacja `quotation.amount` · INSERT `rate_line`/`charge` · live HTTP armatora · LLM liczący spread

### HC

- Kwota wyceny zostaje ze `rate_line` (SQL). Oferta kanału zostaje katalogiem 13.0.
- LLM nie liczy. `charge` zostaje prawdą o marży.
- ExtractionService nie importuje channel_quotes / quotations
