# M-44 różnice kursowe — tabela wycena + kurs NBP

**Moduł żywy:** M-44 (tabela `fx_difference`) + M-21 `quotation` + M-23 `nbp_rate`  
**Plaster:** **101.0** (zamknięty) · fundament tablicy **37.0**  
**Status:** operator **zapisuje** parę wycena + kurs NBP. Kwoty zostają na `charge`. Nie przeliczenie.

Delta: [docs/deltas/archived/101.0-fx-difference.md](../deltas/archived/101.0-fx-difference.md). How-to: [roznica-kursowa.md](../operator/roznica-kursowa.md).

## 101.0 zapis na `/fx-differences`

### Zakres

- Tabela `fx_difference` per tenant: `quotation_id` + `nbp_rate_id` + `source_ref`
- `GET/POST /fx-differences`. Nieznana wycena albo kurs → 404. Pusty `source_ref` → 400
- Ekran `/fx-differences`: lista wierszy + „Zapisz różnicę”. Link do `/quotations` i `/nbp-rates`
- API składa odczyt wyceny i kursu. Serwis różnicy nie importuje innych BC

### Poza 101.0

Przeliczenie · księgowanie FX · kwota na wierszu · para `charge`+kurs · S40 przepływy

### HC

- Marża zostaje w `charge`. Wiersz nie mnoży `amount × mid`.
- LLM nie liczy różnicy kursowej.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje quotations / kursów / charges
