# M-08 charge — buy + sell, marża

**Plaster:** 1.2 DONE · 129.0 `source_ref` leftover P0 · 262.0 GET lista `sell − buy` w SQL · 1.3 = accept HITL → `rate_line` (nie ten spec; `extraction.md`)  
**Status:** fundament (jeden wiersz buy+sell + pochodzenie). Accept HITL nie tworzy `charge` / sell. Brak kolumny magazynu marży.

## Zakres

- Tabela `charge`: `organization_id`, `charge_code` (katalog 1.0), `buy_*` + `sell_*` Numeric(14,4)+CHAR(3), opcjonalny `rate_line_id`, `source_ref` TEXT NULL (stare fixture), obowiązkowy na nowym INSERT, timestamps
- Zapis: `margin(buy, sell)` = sell − buy; ta sama waluta; Decimal; nigdy float / LLM
- GET listy: `sell_amount - buy_amount` w Postgres (262.0); JSON `margin_amount` bez kolumny w tabeli
- CHECK `buy_currency = sell_currency` — integralność, nie drugi wzór
- `rate_line_id` opcjonalny: istniejąca stawka kupna z tym samym `charge_code`
- OpenFGA `can_manage_charges` = member
- UI `/charges`: lista DataTableShell + dodanie

## Poza zakresem

accept HITL → `charge` / sell z LLM, outbox, Wave FE U-*, druga tabela / generated column marży, rollup po `parent_shipment_id` (brak `charge.shipment_id`). 1.3 zapisuje tylko `rate_line` (kupno) z warstwy API.

## HC

- RLS FORCE + test izolacji
- HC-02: `charge` = jedyne miejsce prawdy o marży; kupno i sprzedaż na jednym wierszu
- HC-05: nowy INSERT bez `source_ref` nie wchodzi; walidacja = `require_source_ref`
- ExtractionService nie importuje `rate_lines` / `charges`
