# M-56 RODO — tablica `app_user` (`email`, `display_name`)

**Moduł żywy:** M-56 (token UI `gdpr`, nie tabela) + M-01 `app_user`  
**Plaster:** **46.0** (zamknięty)  
**Status:** operator **widzi** inwentarz kont tenanta. Nie tabela wniosków. Nie usuwanie.

Delta: [docs/deltas/archived/46.0-gdpr.md](../deltas/archived/46.0-gdpr.md).

## 46.0 tablica odczytu na `/gdpr`

### Zakres

- Ekran `/gdpr`: `gdprSubjects` zostawia wiersze z `email`
- Pokazuje `email` i `display_name`
- Link do `/tenancy/users`
- Zero nowej tabeli. Zero `password_hash` na ekranie

### Poza 46.0

Tabela wniosków · usuwanie · DPIA · M-54/M-55 (brak nazwy w PLAN)

### HC

- Marża zostaje w `charge`.
- LLM nie czyta treści ekstrakcji jako inwentarza.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje tenancy
