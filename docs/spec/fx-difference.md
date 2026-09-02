# M-44 różnice kursowe — tablica `nbp_rate` dla walut z `charge` / `quotation`

**Moduł żywy:** M-44 (token UI `fx_difference`, nie tabela) + M-23 `nbp_rate` + M-08 `charge` + M-21 `quotation`  
**Plaster:** **37.0** (zamknięty)  
**Status:** operator **widzi** kurs NBP walut już obecnych na opłacie albo wycenie. Nie tabela. Nie przeliczenie.

Delta: [docs/deltas/archived/37.0-fx-difference.md](../deltas/archived/37.0-fx-difference.md).

## 37.0 tablica odczytu na `/fx-differences`

### Zakres

- Ekran `/fx-differences`: `nbpRatesForKnownCurrencies` filtruje katalog NBP do walut z `charge` i `quotation`
- Zero nowej tabeli. Zero mnożenia. Zero odejmowania kursów

### Poza 37.0

Tabela FX · księgowanie zysku/straty · `amount × mid`

### HC

- Marża zostaje w `charge`. Tablica nie przelicza.
- LLM nie liczy różnicy kursowej.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje nbp_rates / charges / quotations
