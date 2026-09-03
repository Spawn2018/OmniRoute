# M-31 porównanie odpowiedzi — zestawienie i zapis `charge`

**Moduł żywy:** M-31 `response_comparison` + ekran M-21 `/quotations` + katalog M-19 `channel_quote` + M-08 `charge`  
**Plaster:** **84.0** (zamknięty) · 24.0 ślad (zamknięty)  
**Status:** operator **widzi** kwoty na POL/POD i **zapisuje** marżę jako `charge`. Nie odejmowanie w JS. Nie nowa tabela.

Delta: [docs/deltas/archived/84.0-response-comparison-charge.md](../deltas/archived/84.0-response-comparison-charge.md).

## 84.0 spread w `charge`

### Zakres

- Helper `comparisonChargeBody`: kupno z oferty kanału, sprzedaż z wyceny, kod z wyceny
- Na `/quotations`: „Zapisz marżę” w `data-response-comparison="lanes"`
- Marża z `POST /charges` przez `<Money/>` — `margin()` w domenie
- Zero nowej tabeli. Zero nowego endpointu

### Poza 84.0

won/lost · live HTTP · drugi magazyn spread · LLM

### HC

- Panel nie odejmuje kwot. `charge` zostaje prawdą o marży.
- `quotations` service nie importuje `channel_quotes` ani `charges`.
- LLM nie liczy.

## 24.0 zestawienie na POL/POD

Lane wyceny + `channel_quote` o tym samym POL/POD. Obie kwoty przez `<Money/>`.
