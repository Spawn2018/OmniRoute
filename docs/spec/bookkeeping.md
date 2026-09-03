# M-47 księgowość — para opłaty i faktury

**Moduł żywy:** M-47 (tabela `bookkeeping`)  
**Plaster:** **104.0** (S42)  
**Status:** operator **zapisuje**, że ta opłata idzie na tę fakturę. Kwoty zostają na `charge`. Nie JPK.

Delta: [docs/deltas/archived/104.0-bookkeeping.md](../deltas/archived/104.0-bookkeeping.md).

## 104.0 tabela `bookkeeping`

### Zakres

- Tabela `bookkeeping`: `charge_id` + `sales_invoice_id` + `source_ref`
- `GET/POST /bookkeepings`, OpenFGA `can_manage_bookkeeping`
- Ekran `/bookkeeping`: lista wierszy + „Zapisz dekret”
- Zero kwoty na wierszu. Zero `sell − buy`

### Poza 104.0

JPK · HTTP do ERP · plan kont · druga marża

### HC

- Marża zostaje w `charge`. Wiersz nie odejmuje nóg.
- LLM nie liczy dekretu.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje bookkeeping / charges
