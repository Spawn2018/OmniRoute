# M-06 charge_code — katalog

**Plaster:** 1.0  
**Status:** fundament (katalog). Nie `rate_line` (1.1), nie `charge` buy+sell (1.2).

## Zakres

- Tabela `charge_code`: `organization_id`, `code`, `name`, `aliases[]`, timestamps
- Unikalność `(organization_id, code)`; token 2–32 `A-Z0-9_`
- `resolve(token)` — kod albo alias; nieznany token = odrzut (nie luźny string)
- OpenFGA `can_manage_charge_codes` = member
- UI `/charge-codes`: lista DataTableShell + dodanie + rozwiązanie tokenu

## Poza zakresem

`rate_line`, `charge` / marża, accept HITL → stawki, alias jako osobna tabela.

## HC

- RLS FORCE + test izolacji
- Kwoty nie mieszkają na `charge_code`; Money zostaje Decimal (0.25)
- LLM nie liczy
