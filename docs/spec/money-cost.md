# M-43 koszt pieniądza — tabela płatność + kurs NBP

**Moduł żywy:** M-43 (tabela `money_cost`) + M-42 `bank_payment` + M-23 `nbp_rate`  
**Plaster:** **100.0** (zamknięty) · fundament tablicy **36.0**  
**Status:** operator **zapisuje** parę płatność + kurs NBP. Kwoty zostają na `charge`. Nie odsetki. Nie mnożenie.

Delta: [docs/deltas/archived/100.0-money-cost.md](../deltas/archived/100.0-money-cost.md). How-to: [koszt-pieniadza.md](../operator/koszt-pieniadza.md).

## 100.0 zapis na `/money-cost`

### Zakres

- Tabela `money_cost` per tenant: `bank_payment_id` + `nbp_rate_id` + `source_ref`
- `GET/POST /money-costs`. Nieznana płatność albo kurs → 404. Pusty `source_ref` → 400
- Ekran `/money-cost`: lista wierszy + „Zapisz koszt”. Link do `/payments` i `/nbp-rates`
- API składa odczyt płatności i kursu. Serwis kosztu nie importuje innych BC

### Poza 100.0

Odsetki · WACC · mnożenie kursem · kwota na wierszu · `payment_terms_days` · S39 różnice kursowe

### HC

- Marża zostaje w `charge`. Wiersz nie mnoży `buy × mid`.
- LLM nie liczy kosztu pieniądza.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje płatności / kursów / charges
