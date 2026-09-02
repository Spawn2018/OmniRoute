# M-27 wycena wsadowa — wiele kodów na jednej lane

**Moduł żywy:** M-21 `quotation` (pogłębienie) · token `quotation_batch`  
**Plaster:** **20.0** (plan)  
**Status:** plan — jedna transakcja, wiele `charge_code`, ta sama POL/POD/`party_id`. Nie CSV. Nie nowa tabela.

Delta: [docs/deltas/open/20.0-quotation-batch.md](../deltas/open/20.0-quotation-batch.md).

## 20.0 wsad kodów

### Zakres

- `POST /quotations/batch` — `charge_codes` (1–20), lane jak w 5.1
- Serwis woła istniejące `quote_from_current_rate` (kwota z SQL)
- UI na `/quotations`: kody linia po linii, ten sam korytarz
- Luka albo nieznany kod = 400, nic nie commituje

### Poza 20.0

CSV/Excel · Temporal · INSERT set-based (N wywołań SQL leftover) · mutacja `charge` · LLM

### HC

- Kwota ze `rate_line` w SQL. LLM nie liczy.
- ExtractionService nie importuje quotations
