# M-28 zapytania od klientów — ślad wycen per kontrahent

**Moduł żywy:** M-28 (token UI `customer_inquiry`, nie tabela) + ekran M-21 `quotation`  
**Plaster:** **21.0** (plan)  
**Status:** operator **widzi** zapytania jako istniejące wyceny pogrupowane po `party_id`. Nie nowa tabela. Nie IMAP.

Delta: [docs/deltas/open/21.0-customer-inquiry.md](../deltas/open/21.0-customer-inquiry.md).

## 21.0 ślad zapytań z wycen

### Zakres

- Na `/quotations`: panel „Zapytania od klientów” — `party_id` z listy wycen + nazwa z katalogu `party`
- Każda grupa pokazuje kody i kwoty (`<Money/>`) już zapisane na `quotation`
- Zero nowej tabeli. Zero nowego endpointu. Zero sumowania kwot w JS

### Poza 21.0

Tabela RFQ · IMAP (M-32) · status zapytania · auto-INSERT wyceny · M-29 akceptacja · M-30 wysyłka do armatora · LLM

### HC

- Kwota zostaje ze `rate_line` (SQL). Panel nic nie liczy.
- LLM nie liczy. `charge` zostaje prawdą o marży.
- ExtractionService nie importuje quotations
