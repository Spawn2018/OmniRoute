# M-40 fakturowanie — tablica sprzedaży z `charge`

**Moduł żywy:** M-40 (token UI `sales_invoice`, nie tabela) + ekran M-08 `charge`  
**Plaster:** **33.0** (zamknięty)  
**Status:** operator **widzi** `sell_amount` z `charge`. Nie KSeF. Nie nowa tabela.

Delta: [docs/deltas/archived/33.0-sales-invoice.md](../deltas/archived/33.0-sales-invoice.md).

## 33.0 tablica odczytu na `/invoices`

### Zakres

- Ekran `/invoices`: lista `charge` z kwotą sprzedaży przez `<Money/>`
- Link do `/charges` i `/finance`. Zero nowej tabeli. Zero KSeF. Zero odejmowania w JS

### Poza 33.0

Tabela faktur · KSeF · U-print · rozliczenie z wyceną (M-41) · numer FV

### HC

- Marża zostaje w `charge`. Tablica nie odejmuje buy/sell.
- LLM nie pisze treści faktury.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje charges
