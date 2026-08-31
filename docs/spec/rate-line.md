# M-07 rate_line — stawka kupna

**Plaster:** 1.1  
**Status:** fundament (niemutowalna stawka + provenance). Nie `charge` buy+sell (1.2). Nie accept HITL → stawki (1.3).

## Zakres

- Tabela `rate_line`: `organization_id`, `charge_code` (token z katalogu 1.0), `amount` Numeric(14,4) + `currency` CHAR(3), `source_ref`, `superseded_by`, timestamps
- `source_ref` obowiązkowy; puste / sam whitespace = odrzut
- Kwota tylko przez `Money` (Decimal + ISO); JSON `amount` jako tekst, nie float
- Zmiana = nowy wiersz + `superseded_by` na poprzedniku; trigger blokuje UPDATE kwoty/waluty/`source_ref` i DELETE
- OpenFGA `can_manage_rate_lines` = member
- UI `/rate-lines`: lista DataTableShell + dodanie + zastąpienie

## Poza zakresem

`charge` / marża (1.2), accept HITL → RatesService (1.3), outbox, Wave FE U-*.

## HC

- RLS FORCE + test izolacji
- HC-02: nigdy float; LLM nie liczy
- HC-03: bez `source_ref` stawka nie wchodzi; niemutowalność
