# M-21 quotation — silnik wyceny SQL

**Plaster:** 2.0  
**Status:** fundament (wycena z bieżącego `rate_line` w SQL). Nie marża. Nie k6.

## Zakres

- Tabela `quotation`: snapshot `organization_id`, `charge_code`, `rate_line_id`, `amount` Numeric(14,4) + `currency` CHAR(3), `source_ref`, timestamps
- INSERT…SELECT z `rate_line` gdzie `superseded_by IS NULL`; kwota tylko ze stawki, nigdy z requestu / LLM / Pythona
- Brak bieżącej stawki = `quotation_gap` (luka wyceny)
- `charge_code` z katalogu 1.0; nie luźny string
- OpenFGA `can_manage_quotations` = member
- UI `/quotations`: lista DataTableShell + wycena po kodzie opłaty

## Poza zakresem

`charge` / `margin()`, accept HITL, outbox, k6, Wave FE claim, druga tabela marży.

## HC

- RLS FORCE + test izolacji
- HC-02: Decimal + ISO; LLM nie liczy
- HC-07: dobór stawki w SQL, nie ORM na 50k wierszy
- ExtractionService nie importuje quotations / rates
