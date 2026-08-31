# M-08 charge — buy + sell, marża

**Plaster:** 1.2  
**Status:** fundament (jeden wiersz buy+sell). Nie accept HITL → RatesService (1.3).

## Zakres

- Tabela `charge`: `organization_id`, `charge_code` (katalog 1.0), `buy_*` + `sell_*` Numeric(14,4)+CHAR(3), opcjonalny `rate_line_id`, timestamps
- Jedyna funkcja marży: `margin(buy, sell)` = sell − buy; ta sama waluta; Decimal; nigdy float / LLM
- CHECK `buy_currency = sell_currency` — integralność, nie drugi wzór
- `rate_line_id` opcjonalny: istniejąca stawka kupna z tym samym `charge_code`
- OpenFGA `can_manage_charges` = member
- UI `/charges`: lista DataTableShell + dodanie

## Poza zakresem

accept HITL → RatesService (1.3), outbox, Wave FE U-*, druga tabela marży.

## HC

- RLS FORCE + test izolacji
- HC-02: `charge` = jedyne miejsce prawdy o marży; kupno i sprzedaż na jednym wierszu
- ExtractionService nie importuje `rate_lines` / `charges`
