# M-15 finance_board — Wirtualny Dyrektor Finansowy (tablica faktów)

**Moduł żywy:** M-15  
**Plaster:** **15.0** (zamknięty)  
**Status:** tablica odczytu `/finance`. Nie silnik AI. LLM nie liczy.

Delta: [docs/deltas/archived/15.0-finance-board.md](../deltas/archived/15.0-finance-board.md).

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
