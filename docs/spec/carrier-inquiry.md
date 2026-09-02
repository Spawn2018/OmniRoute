# M-30 zapytania do armatorów — ślad `channel_quote` przy wycenie

**Moduł żywy:** M-30 (token UI `carrier_inquiry`, nie tabela) + ekran M-21 `quotation` + katalog M-19 `channel_quote`  
**Plaster:** **23.0** (zamknięty)  
**Status:** operator **widzi** oferty kanału pasujące do lane wyceny. Nie wysyłka HTTP. Nie nowa tabela RFQ.

Delta: [docs/deltas/archived/23.0-carrier-inquiry.md](../deltas/archived/23.0-carrier-inquiry.md).

## 23.0 ślad z katalogu kanału

### Zakres

- Na `/quotations`: panel „Zapytania do armatorów” — `fetchChannelQuotes` + dopasowanie do lane wyceny (`party_id` + POL/POD)
- Kwota oferty przez `<Money/>`. Zero odejmowania od wyceny
- Zero nowej tabeli. Zero live HTTP. Zero IMAP

### Poza 23.0

Tabela RFQ · adapter armatora · sekrety tenanta · M-31 silnik porównania · zapis do `rate_line`/`charge` · LLM

### HC

- Kwoty zostają w katalogu `channel_quote` i w `quotation` (SQL). Panel nic nie liczy.
- `quotations` service nie importuje `channel_quotes`.
- LLM nie liczy. `charge` zostaje prawdą o marży.
- ExtractionService nie importuje channel_quotes / quotations
