# M-45 przepływy — para wyceny i płatności

**Moduł żywy:** M-45 (tabela `cash_flow`)  
**Plaster:** **102.0** (S40)  
**Status:** operator **zapisuje**, że ta wycena ma ruch pieniądza w tej płatności. Kwoty zostają na `charge`. Nie odejmowanie.

Delta: [docs/deltas/archived/102.0-cash-flow.md](../deltas/archived/102.0-cash-flow.md).

## 102.0 tabela `cash_flow`

### Zakres

- Tabela `cash_flow`: `quotation_id` + `bank_payment_id` + `source_ref`
- `GET/POST /cash-flows`, OpenFGA `can_manage_cash_flows`
- Ekran `/cashflows`: lista wierszy + „Zapisz przepływ”
- Zero kwoty na wierszu. Zero `sell − buy`

### Poza 102.0

DSO · dopasowanie wyciągu · para `charge`+płatność · druga marża

### HC

- Marża zostaje w `charge`. Wiersz nie odejmuje nóg.
- LLM nie liczy przepływu.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje cash_flows / quotations / charges
