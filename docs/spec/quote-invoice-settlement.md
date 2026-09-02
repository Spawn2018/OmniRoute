# M-41 rozliczenie wyceny z fakturą — tablica `quotation` + `sell` z `charge`

**Moduł żywy:** M-41 (token UI `quote_invoice_settlement`, nie tabela) + ekrany M-21 `quotation` i M-40 `sales_invoice`  
**Plaster:** **34.0** (zamknięty)  
**Status:** operator **widzi** wycenę i sprzedaż z `charge` przy wspólnym `rate_line_id`. Nie tabela. Nie odejmowanie.

Delta: [docs/deltas/archived/34.0-quote-invoice-settlement.md](../deltas/archived/34.0-quote-invoice-settlement.md).

## 34.0 tablica odczytu na `/quote-invoices`

### Zakres

- Ekran `/quote-invoices`: `quotationInvoiceSettlements(quotations, charges)` po `rate_line_id`
- Kwota wyceny i `sell_amount` przez `<Money/>`. Link do `/quotations` i `/invoices`
- Zero nowej tabeli. Zero FK. Zero odejmowania w JS

### Poza 34.0

Tabela rozliczenia · `quotation_id` na `charge` · KSeF · numer FV · SQL-refresh `quote_invoice_match_rate`

### HC

- Marża zostaje w `charge`. Tablica nie odejmuje kwot.
- LLM nie liczy różnicy wycena vs FV.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje quotations / charges
