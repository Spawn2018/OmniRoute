# M-06 charge_code — katalog

**Plaster:** 1.0  
**Status:** fundament (katalog). Nie `rate_line` (1.1), nie `charge` buy+sell (1.2).

## Zakres

- Tabela `charge_code`: `organization_id`, `code`, `name`, `aliases[]`, `source_ref`, timestamps
- Unikalność `(organization_id, code)`; token 2–32 `A-Z0-9_`
- `source_ref` wymagany (1–512); backfill legacy `fixture://charge-code/legacy`
- WAITING / NO_SHOW / DIVERSION / STAMP wolne jak każdy token — bez CHECK allowlisty; seed Omni = leftover
- `resolve(token)` — kod albo alias; nieznany token = odrzut (nie luźny string)
- OpenFGA `can_manage_charge_codes` = member
- UI `/charge-codes`: lista DataTableShell + dodanie + `source_ref` + rozwiązanie tokenu

## Poza zakresem

`rate_line`, `charge` / marża, accept HITL → stawki, alias jako osobna tabela.

## HC

- RLS FORCE + test izolacji
- Kwoty nie mieszkają na `charge_code`; Money zostaje Decimal (0.25)
- LLM nie liczy
