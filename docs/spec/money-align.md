# U-money-align — oś dziesiętna na `<Money/>`

**Leftover żywy:** U-money-align (PLAN § Wave FE, token UI `money_axis`, nie tabela)  
**Plaster:** **52.0** (plan)  
**Status:** operator **zobaczy** kwotę wyrównaną do przecinka + kod waluty. Nie float. Nie nowa tabela.

Delta: [docs/deltas/open/52.0-money-align.md](../deltas/open/52.0-money-align.md).

## 52.0 siatka na `<Money/>`

### Zakres

- `moneyAxis` rozcina wynik `parseMoney` na integer / 4 miejsca / ISO
- `<Money/>`: `data-money="axis"`; `lining-nums tabular-nums`
- Tekst HITL poza decimal zostaje bez fałszywej osi
- Zero nowej tabeli i trasy

### Poza 52.0

Grupowanie tysięcy przez locale · condensed · i18n klucze

### HC

- Marża zostaje w `charge`.
- LLM nie liczy.
- Kwota zostaje `string` + Decimal w bazie.
- Zakaz `parseFloat`.
