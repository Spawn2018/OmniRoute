# M-53 sankcje — tablica `party` z `tax_id` i `country_code`

**Moduł żywy:** M-53 (token UI `sanctions`, nie tabela) + M-10 `party`  
**Plaster:** **45.0** (plan)  
**Status:** operator **zobaczy** aktywnych kontrahentów do ręcznego przeglądu. Nie tabela OFAC. Nie HTTP.

Delta: [docs/deltas/open/45.0-sanctions.md](../deltas/open/45.0-sanctions.md).

## 45.0 tablica odczytu na `/sanctions`

### Zakres

- Ekran `/sanctions`: `sanctionsParties` zostawia `is_active`
- Pokazuje `legal_name`, `tax_id`, `country_code`
- Link do `/parties`
- Zero nowej tabeli

### Poza 45.0

Tabela hitów · HTTP OFAC/EU · auto-match · lista krajów w kodzie

### HC

- Marża zostaje w `charge`.
- LLM nie scoruje osoby.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje parties
