# M-41 rozliczenie wyceny z fakturą — tabela pary

**Moduł żywy:** M-41 (tabela `quote_invoice_settlement`) + ekrany M-21 `quotation` i M-40 `sales_invoice`  
**Plaster:** **98.0** (S36) po fundamencie **34.0**  
**Status:** operator **zapisuje** parę wycena + faktura. Kwoty zostają na `charge`. Nie odejmowanie.

Delta: [docs/deltas/archived/98.0-quote-invoice-settlement.md](../deltas/archived/98.0-quote-invoice-settlement.md). Fundament: [docs/deltas/archived/34.0-quote-invoice-settlement.md](../deltas/archived/34.0-quote-invoice-settlement.md).

## 34.0 tablica odczytu na `/quote-invoices`

Zastąpiona w 98.0. Historycznie: lista wyceny i `sell_amount` z `charge` po `rate_line_id` bez tabeli.

## 98.0 tabela na `/quote-invoices`

### Zakres

- Tabela `quote_invoice_settlement` per tenant, FK do `quotation` i `sales_invoice`, RLS FORCE
- Ekran `/quote-invoices`: lista wierszy + „Zapisz rozliczenie”. Link do `/quotations` i `/invoices`
- `source_ref` obowiązkowy. Unikat pary wycena+faktura w tenancie

### Poza 98.0

Kwota / marża na wierszu · `quotation_id` na `charge` · match do `shipment.quotation_id` · `quote_invoice_match_rate` · S37 bank · F9.1

### HC

- Marża zostaje w `charge`. Wiersz rozliczenia nie niesie kwoty.
- LLM nie liczy różnicy wycena vs FV.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje rozliczeń ani quotations
