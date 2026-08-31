# M-08 charge — buy + sell, marża

**Plaster:** 1.2 DONE · 1.3 = accept HITL → `rate_line` (nie ten spec; `extraction.md`)  
**Status:** fundament (jeden wiersz buy+sell). Accept HITL nie tworzy `charge` / sell.

## Zakres

- Tabela `charge`: `organization_id`, `charge_code` (katalog 1.0), `buy_*` + `sell_*` Numeric(14,4)+CHAR(3), opcjonalny `rate_line_id`, timestamps
- Jedyna funkcja marży: `margin(buy, sell)` = sell − buy; ta sama waluta; Decimal; nigdy float / LLM
- CHECK `buy_currency = sell_currency` — integralność, nie drugi wzór
- `rate_line_id` opcjonalny: istniejąca stawka kupna z tym samym `charge_code`
- OpenFGA `can_manage_charges` = member
- UI `/charges`: lista DataTableShell + dodanie

## Poza zakresem

accept HITL → `charge` / sell z LLM, outbox, Wave FE U-*, druga tabela marży. 1.3 zapisuje tylko `rate_line` (kupno) z warstwy API.

## HC

- RLS FORCE + test izolacji
- HC-02: `charge` = jedyne miejsce prawdy o marży; kupno i sprzedaż na jednym wierszu
- ExtractionService nie importuje `rate_lines` / `charges`
