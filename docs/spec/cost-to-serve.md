# M-46 koszt obsługi klienta — para SOP i wyceny

**Moduł żywy:** M-46 (tabela `cost_to_serve`)  
**Plaster:** **103.0** (S41)  
**Status:** operator **zapisuje**, że ta wycena szła pod tą procedurą klienta. Kwoty zostają na `quotation` / `charge`. Nie suma.

Delta: [docs/deltas/archived/103.0-cost-to-serve.md](../deltas/archived/103.0-cost-to-serve.md).

## 103.0 tabela `cost_to_serve`

### Zakres

- Tabela `cost_to_serve`: `customer_sop_id` + `quotation_id` + `source_ref`
- `GET/POST /cost-to-serves`, OpenFGA `can_manage_cost_to_serve`
- Ekran `/cost-to-serve`: lista wierszy + „Zapisz koszt obsługi”
- Zero kwoty na wierszu. Zero sumy wycen

### Poza 103.0

ABC · stawka godziny · suma wycen · `party_id` na `charge`

### HC

- Marża zostaje w `charge`. Wiersz nie sumuje wycen.
- LLM nie liczy kosztu obsługi.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje cost_to_serve / parties / quotations
