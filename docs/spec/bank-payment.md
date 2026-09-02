# M-42 bank i płatności — tablica IBAN + `sell` z `charge`

**Moduł żywy:** M-42 (token UI `bank_payment`, nie tabela) + katalog M-10 `party_bank_account` + M-08 `charge`  
**Plaster:** **35.0** (zamknięty)  
**Status:** operator **widzi** rachunek kontrahenta i sprzedaż z `charge`. Nie tabela płatności. Nie odejmowanie.

Delta: [docs/deltas/archived/35.0-bank-payment.md](../deltas/archived/35.0-bank-payment.md).

## 35.0 tablica odczytu na `/payments`

### Zakres

- Ekran `/payments`: wybór `party` + lista `party_bank_account` + `iban-lookup` + `sell_amount` z `charge`
- Kwota przez `<Money/>`. Link do `/parties` i `/invoices`
- Zero nowej tabeli. Zero N+1. Zero odejmowania w JS

### Poza 35.0

Tabela płatności · SEPA · wyciąg · PSD2 · zapis IBAN z tego ekranu

### HC

- Marża zostaje w `charge`. Tablica nie odejmuje kwot.
- LLM nie liczy salda.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje parties / charges
