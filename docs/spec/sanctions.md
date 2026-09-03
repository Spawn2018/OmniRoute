# M-53 sankcje — tablica `party` z `tax_id` i `country_code`

**Moduł żywy:** M-53 (token UI `sanctions`, nie tabela) + M-10 `party`  
**Plaster:** **45.0** (tablica) · **89.0** (sprawdzenie na `party`)  
**Status:** operator widzi aktywnych kontrahentów i zapisuje wskazanie listy na karcie. Nie tabela hitów. Nie live lista. Nie auto-match.

Delta: [docs/deltas/archived/45.0-sanctions.md](../deltas/archived/45.0-sanctions.md) · [docs/deltas/archived/89.0-party-sanctions-screen.md](../deltas/archived/89.0-party-sanctions-screen.md).

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

## 89.0 sprawdzenie listy na party

### Zakres

- `party.sanctions_list_ref` + `sanctions_checked_at`. RLS z 015.
- `POST /parties/{id}/screen-sanctions`. Prefix `fixture://sanctions/` albo `eu://`.
- UI `/sanctions`: „Zapisz sprawdzenie”. `source_ref` i `credit_limit` nietknięte.

### Poza 89.0

Live lista · auto-match · tabela hitów · S27b · S28
