# M-39 EDI — tablica `channel_quote` na lane wyceny

**Moduł żywy:** M-39 (token UI `edi_message`, nie tabela) + ekrany M-19 `channel_quote` i M-21 `quotation`  
**Plaster:** **32.0** (zamknięty)  
**Status:** operator **widzi** oferty kanału dopasowane do lane wyceny. Nie X12. Nie nowa tabela.

Delta: [docs/deltas/archived/32.0-edi-message.md](../deltas/archived/32.0-edi-message.md).

## 32.0 tablica odczytu na `/edi`

### Zakres

- Ekran `/edi`: `quotationCarrierInquiries(quotationLanes(quotations), channelQuotes)`
- Kwota przez `<Money/>`. Link do `/channel-quotes` i `/quotations`
- Zero nowej tabeli. Zero parsera. Zero live HTTP

### Poza 32.0

Tabela EDI · X12 / EDIFACT · IFTMIN · live HTTP · outbox

### HC

- Marża zostaje w `charge`. Tablica nie odejmuje kwot.
- LLM nie składa komunikatu.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje quotations / channel_quotes
