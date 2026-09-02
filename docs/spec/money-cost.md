# M-43 koszt pieniądza — tablica `nbp_rate` + `buy` z `charge`

**Moduł żywy:** M-43 (token UI `money_cost`, nie tabela) + katalog M-23 `nbp_rate` + M-08 `charge`  
**Plaster:** **36.0** (zamknięty)  
**Status:** operator **widzi** kurs NBP i kupno z `charge`. Nie tabela odsetek. Nie mnożenie.

Delta: [docs/deltas/archived/36.0-money-cost.md](../deltas/archived/36.0-money-cost.md).

## 36.0 tablica odczytu na `/money-cost`

### Zakres

- Ekran `/money-cost`: lista `nbp_rate` oraz `buy_amount` z `charge` przez `<Money/>`
- Link do `/nbp-rates` i `/charges`
- Zero nowej tabeli. Zero mnożenia `buy × mid`

### Poza 36.0

Tabela odsetek · WACC · `payment_terms_days` w API · zapis kursu

### HC

- Marża zostaje w `charge`. Tablica nie mnoży kwot kursem.
- LLM nie liczy kosztu pieniądza.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje nbp_rates / charges
