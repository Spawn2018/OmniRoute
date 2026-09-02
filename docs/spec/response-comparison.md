# M-31 porównanie odpowiedzi — zestawienie wyceny i `channel_quote` na POL/POD

**Moduł żywy:** M-31 (token UI `response_comparison`, nie tabela) + ekran M-21 `quotation` + katalog M-19 `channel_quote`  
**Plaster:** **24.0** (plan)  
**Status:** operator **widzi** kwoty wyceny i odpowiedzi kanałów na tej samej parze portów. Nie odejmowanie. Nie nowa tabela.

Delta: [docs/deltas/open/24.0-response-comparison.md](../deltas/open/24.0-response-comparison.md).

## 24.0 zestawienie na POL/POD

### Zakres

- Na `/quotations`: panel „Porównanie odpowiedzi” — lane wyceny + `channel_quote` o tym samym POL/POD
- Obie kwoty przez `<Money/>`. Zero odejmowania w JS
- Zero nowej tabeli. Zero endpointu spread. Zero live HTTP

### Poza 24.0

Silnik różnicy Decimal (SQL/Python) · katalog `won`/`lost` · IMAP (M-32) · zapis do `rate_line`/`charge` · LLM

### HC

- Kwoty zostają w `quotation` i `channel_quote` (SQL). Panel nic nie liczy.
- `quotations` service nie importuje `channel_quotes`.
- LLM nie liczy. `charge` zostaje prawdą o marży.
- ExtractionService nie importuje channel_quotes / quotations
