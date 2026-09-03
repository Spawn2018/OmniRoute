# M-15 finance_board — Wirtualny Dyrektor Finansowy (tablica faktów)

**Moduł żywy:** M-15  
**Plaster:** **15.0** (zamknięty) · **106.0** (S44 plan)  
**Status:** tablica odczytu `/finance`, w tym faktury. Nie silnik AI. LLM nie liczy.

Delta 15.0: [docs/deltas/archived/15.0-finance-board.md](../deltas/archived/15.0-finance-board.md).  
Delta 106.0: [docs/deltas/open/106.0-finance-board-invoices.md](../deltas/open/106.0-finance-board-invoices.md).

## 15.0 tablica faktów

### Zakres

- Ekran operatora `/finance`: marże z katalogu `charge` (już w API jako `margin_amount` / `margin_currency`), kursy `nbp_rate`, limity `party.credit_limit` (odczyt), recenzje `credit_review`
- Zero nowej tabeli. Zero nowej kolumny. Zero nowego BC `app.services.*`
- Kwoty tylko przez `<Money/>` z tekstu dziesiętnego z API — JS nie odejmuje buy/sell

### Poza 15.0

LLM komentujący marżę · nowa tabela `finance_*` · liczenie w Pythonie/JS · zapis `credit_limit` · auto-scoring · mutacja `charge` · ExtractionService · portal · Auth0 · M-02

### HC

- `charge` zostaje prawdą o marży
- LLM nie liczy
- Brak zgadywania schematu VDF z archiwum — 15.0 nie wymyśla silnika

## 106.0 faktury na tablicy

### Zakres

- `/finance` czyta `sales_invoice` (`invoice_ref`, `invoice_kind`, `ksef_ref`)
- Zero nowej tabeli. Zero kwoty na tym bloku.

### Poza 106.0

Narracja NL (S57) · silnik limitu · suma FV · collective_invoice na tablicy
