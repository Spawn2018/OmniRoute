# M-52 dangerous_good — katalog towarów niebezpiecznych

**Plaster:** 7.0 (delta `docs/deltas/open/7.0-dangerous-good.md`)  
**Status:** planowany katalog numeru UN + klasy IMDG per tenant. Nie podpięcie do wyceny. Nie żywe M-08 `charge`.

## Zakres

- Tabela `dangerous_good`: `organization_id`, `un_number` (4 cyfry), `imdg_class` (allowlista IMDG), `name`, `aliases[]`, `source_ref`, timestamps
- Unikalność `(organization_id, un_number)`
- `resolve(token)` — numer UN albo alias; nieznany = `UnknownDangerousGood`
- OpenFGA `can_manage_dangerous_goods` = member
- UI `/dangerous-goods`: lista DataTableShell + dodanie + rozwiązanie tokenu

## Poza zakresem

`quotation` / `commodity_code` z FK · ADN/ADR jako osobne tabele · grupy zgodności 1.xA · packing group · live IMO · nadpisanie M-08 `charge`

## HC

- RLS FORCE + test izolacji
- Kwoty nie mieszkają na katalogu
- LLM nie liczy i nie nadaje klasy IMDG
- ExtractionService nie importuje `dangerous_goods`
