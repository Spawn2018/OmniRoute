# M-45 przepływy — tablica `buy` i `sell` z `charge`

**Moduł żywy:** M-45 (token UI `cash_flow`, nie tabela) + M-08 `charge`  
**Plaster:** **38.0** (do `/plaster`)  
**Status:** operator **widzi** wypływ (`buy`) i wpływ (`sell`) z istniejącej opłaty. Nie tabela księgi. Nie odejmowanie.

Delta: [docs/deltas/open/38.0-cash-flow.md](../deltas/open/38.0-cash-flow.md).

## 38.0 tablica odczytu na `/cashflows`

### Zakres

- Ekran `/cashflows`: `cashFlowLegs` mapuje `charge` na wypływ (`buy`) i wpływ (`sell`)
- Link do `/charges`
- Zero nowej tabeli. Zero `sell − buy` w JS

### Poza 38.0

Tabela księgi · DSO · dopasowanie wyciągu · druga marża

### HC

- Marża zostaje w `charge`. Tablica nie odejmuje nóg.
- LLM nie liczy przepływu.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje charges
