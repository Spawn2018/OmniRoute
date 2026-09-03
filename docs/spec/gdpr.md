# M-56 RODO — inwentarz kont i wniosek (`gdpr_request`)

**Moduł żywy:** M-56 (token UI `gdpr`) + tabela `gdpr_request` + M-01 `app_user`  
**Plaster:** **46.0** (zamknięty) · **107.0** (zamknięty)  
**Status:** operator widzi inwentarz kont i zapisuje wniosek access/erasure. Nie DPIA. Nie kasowanie innych BC.

Delta 46.0: [docs/deltas/archived/46.0-gdpr.md](../deltas/archived/46.0-gdpr.md).  
Delta 107.0: [docs/deltas/archived/107.0-gdpr-request.md](../deltas/archived/107.0-gdpr-request.md).

## 46.0 tablica odczytu na `/gdpr`

### Zakres

- Ekran `/gdpr`: `gdprSubjects` zostawia wiersze z `email`
- Pokazuje `email` i `display_name`
- Link do `/tenancy/users`
- Zero `password_hash` na ekranie

### Poza 46.0

DPIA · M-54/M-55 (brak nazwy w PLAN) · kasowanie inbound/party

### HC

- Marża zostaje w `charge`.
- LLM nie czyta treści ekstrakcji jako inwentarza.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje tenancy

## 107.0 wniosek i usunięcie katalogu

### Zakres

- Tabela `gdpr_request` (RLS) na tym samym `/gdpr`
- `access` = wypełnienie bez zmiany konta
- `erasure` = tombstone `app_user` (email / display_name / password_hash), bez `DELETE` wiersza

### Poza 107.0

DPIA · zgody · kasowanie inbound/party/extract · portal osoby · unieważnienie JWT
