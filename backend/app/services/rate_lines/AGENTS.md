# BC rate_line (M-07)

Niemutowalna stawka kupna + `source_ref` + opcjonalny HITL `allotment_teu` +
opcjonalny HITL `spot_or_contract` + opcjonalny HITL `index_id` + opcjonalny
HITL `fuel_index_id` (FK katalogu P3). Nie tabela `charge`, nie accept HITL.

## Dozwolone zależności
- `app.models.rate_line`
- `app.repositories.rate_lines`
- `app.repositories.charge_codes` — odczyt katalogu, nie zapis
- `app.repositories.fuel_indexes` — odczyt katalogu, nie zapis
- `app.domain`

## Zakaz
- import innych BC services (w tym `fuel_indexes`)
- zapis `charge` / marża
- zapis z `ExtractionService`
- mutacja `amount` / `currency` / `source_ref` / `allotment_teu` /
  `spot_or_contract` / `index_id` / `fuel_index_id` w miejscu
- float / matching WHEN/IF
- mnożenie TEU × amount
- mnożenie FSC × amount / przeliczenie na `charge`
