# M-42 bank i płatności — tabela faktura + rachunek

**Moduł żywy:** M-42 (tabela `bank_payment`) + katalog M-10 `party_bank_account` + M-40 `sales_invoice`  
**Plaster:** **99.0** (zamknięty) · fundament tablicy **35.0**  
**Status:** operator **zapisuje** parę faktura + rachunek. Kwoty zostają na `charge`. Nie SEPA. Nie odejmowanie.

Delta: [docs/deltas/archived/99.0-bank-payment.md](../deltas/archived/99.0-bank-payment.md). How-to: [platnosc.md](../operator/platnosc.md).

## 99.0 zapis na `/payments`

### Zakres

- Tabela `bank_payment` per tenant: `sales_invoice_id` + `party_bank_account_id` + `source_ref`
- `GET/POST /bank-payments`. Nieznana faktura albo rachunek → 404. Pusty `source_ref` → 400
- Ekran `/payments`: lista wierszy + „Zapisz płatność”. Link do `/parties` i `/invoices`
- API składa odczyt faktury i rachunku. Serwis płatności nie importuje innych BC

### Poza 99.0

SEPA · wyciąg · PSD2 · kwota na wierszu · zapis IBAN z tego ekranu · S38 koszt pieniądza

### HC

- Marża zostaje w `charge`. Wiersz nie kopiuje `sell`.
- LLM nie liczy salda.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje płatności / invoices / parties
