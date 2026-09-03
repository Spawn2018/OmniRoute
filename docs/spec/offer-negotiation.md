# M-25 negocjacja i wynik — odczyt i wskazanie `channel_quote` przy `quotation`

**Moduł żywy:** M-25 (token `offer_negotiation`) + ekran M-21 `quotation`  
**Plaster:** **18.0** (odczyt) · **85.0** (wskazanie)  
**Status:** wycena **czyta** katalog 13.0 i **zapisuje** `negotiated_channel_quote_id`. Nie won/lost. Nie odejmowanie kwot.

Delta: [18.0](../deltas/archived/18.0-offer-negotiation.md) · [85.0](../deltas/archived/85.0-offer-negotiation-result.md).

## 18.0 oferta kanału przy wycenie

### Zakres

- Na `/quotations`: panel „Oferta kanału przy wycenie” — wiersz z `party_id` + POL + POD
- `resolveChannelQuote` (armator, POL, POD, dzień)
- Pokazuje kwotę kanału i kwotę wyceny osobno (`<Money/>`) — bez różnicy w JS
- Zero nowej tabeli. Zero importu `channel_quotes` z `quotations` service

### Poza 18.0

Katalog `won`/`lost` · mutacja `quotation.amount` · INSERT `rate_line`/`charge` · live HTTP armatora · LLM liczący spread

## 85.0 wskazanie oferty kanału

### Zakres

- Kolumna `quotation.negotiated_channel_quote_id` (UUID NULL, bez nowej kwoty)
- `PATCH /quotations/{id}/negotiate` — API składa: `ChannelQuoteService.get_quote`, potem zapis UUID
- UI „Zapisz wynik” w panelu 18.0
- Serwis `quotations` nie importuje `channel_quotes` / `charges`

### Poza 85.0

won/lost · mutacja `quotation.amount` · nowy `margin` · live HTTP · F9.1

## HC

- Kwota wyceny zostaje ze `rate_line` (SQL). Oferta kanału zostaje katalogiem 13.0.
- Wskazanie nie zastępuje `margin()`.
- LLM nie liczy. `charge` zostaje prawdą o marży.
- ExtractionService nie importuje channel_quotes / quotations
