# M-47 księgowość — tablica `charge` z nazwą z `charge_code`

**Moduł żywy:** M-47 (token UI `bookkeeping`, nie tabela) + M-06 `charge_code` + M-08 `charge`  
**Plaster:** **40.0** (do `/plaster`)  
**Status:** operator **widzi** kod, nazwę katalogu oraz kupno/sprzedaż. Nie JPK. Nie ERP.

Delta: [docs/deltas/open/40.0-bookkeeping.md](../deltas/open/40.0-bookkeeping.md).

## 40.0 tablica odczytu na `/bookkeeping`

### Zakres

- Ekran `/bookkeeping`: `bookkeepingLines` łączy `charge` z `charge_code.name`
- Link do `/charge-codes` i `/charges`
- Zero nowej tabeli. Zero pliku. Zero `sell − buy` w JS

### Poza 40.0

JPK · HTTP do ERP · tabela dekretów · druga marża

### HC

- Marża zostaje w `charge`. Tablica nie odejmuje.
- LLM nie liczy dekretu.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje charges
