# M-46 koszt obsługi klienta — tablica `customer_sop` i wycen kontrahenta

**Moduł żywy:** M-46 (token UI `cost_to_serve`, nie tabela) + M-16 `customer_sop` + M-21 `quotation`  
**Plaster:** **39.0** (do `/plaster`)  
**Status:** operator **widzi** procedury i wyceny wybranego kontrahenta. Nie tabela ABC. Nie suma kwot.

Delta: [docs/deltas/open/39.0-cost-to-serve.md](../deltas/open/39.0-cost-to-serve.md).

## 39.0 tablica odczytu na `/cost-to-serve`

### Zakres

- Ekran `/cost-to-serve`: jeden `party`; `customerSopsForParty`; wyceny z `fetchQuotations` po `party_id`
- Link do `/customer-sops` i `/quotations`
- Zero nowej tabeli. Zero sumy kwot

### Poza 39.0

Tabela ABC · stawka godziny · suma wycen · `party_id` na `charge`

### HC

- Marża zostaje w `charge`. Tablica nie sumuje wycen.
- LLM nie liczy kosztu obsługi.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje parties / quotations
