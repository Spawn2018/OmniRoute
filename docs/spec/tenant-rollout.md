# M-70 wdrożenie — tablica `organization_setting` na allowliście

**Moduł żywy:** M-70 (token UI `tenant_rollout`, nie tabela) + M-03 `organization_setting`  
**Plaster:** **50.0** (plan)  
**Status:** operator **zobaczy** klucz `default_currency`. Nie tabela rollout. Nie upsert.

Delta: [docs/deltas/open/50.0-tenant-rollout.md](../deltas/open/50.0-tenant-rollout.md).

## 50.0 tablica odczytu na `/rollout`

### Zakres

- Ekran `/rollout`: `rolloutSettings` zostawia wiersze z `setting_key` `default_currency`
- Pokazuje klucz i wartość; nie formularz zapisu
- Link do `/organization-settings`
- Zero nowej tabeli

### Poza 50.0

Tabela rollout · CI/CD · sekrety · Auth0

### HC

- Marża zostaje w `charge`.
- LLM nie liczy gotowości.
- Konfiguracja zostaje danymi, nie env.
- HITL zostaje.
