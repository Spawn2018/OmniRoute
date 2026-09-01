# M-09 commodity_code — katalog kodów towarowych

**Plaster:** 5.2 (delta `docs/deltas/open/5.2-commodity-code.md`)  
**Status:** planowany katalog HS/CN per tenant. Nie podpięcie do wyceny. Nie IMDG (Q6).

## Zakres

- Tabela `commodity_code`: `organization_id`, `code` (4–10 cyfr), `name`, `aliases[]`, `source_ref`, timestamps
- Unikalność `(organization_id, code)`
- `resolve(token)` — kod albo alias; nieznany = `UnknownCommodityCode`
- OpenFGA `can_manage_commodity_codes` = member
- UI `/commodity-codes`: lista DataTableShell + dodanie + rozwiązanie tokenu

## Poza zakresem

`quotation` / `rate_line` z FK do kodu, TARIC live, towary niebezpieczne (Q6), osobna tabela aliasów.

## HC

- RLS FORCE + test izolacji
- Kwoty nie mieszkają na katalogu
- LLM nie liczy
- ExtractionService nie importuje commodity_codes
