# M-09 commodity_code — katalog kodów towarowych

**Plaster:** 5.2 (delta `docs/deltas/archived/5.2-commodity-code.md`)  
**Status:** katalog HS/CN per tenant. 70.0 podpina `commodity_code_id` do RFQ i wyceny. Nie IMDG.

## Zakres

- Tabela `commodity_code`: `organization_id`, `code` (4–10 cyfr), `name`, `aliases[]`, `source_ref`, timestamps
- Unikalność `(organization_id, code)`
- `resolve(token)` — kod albo alias; nieznany = `UnknownCommodityCode`
- OpenFGA `can_manage_commodity_codes` = member
- UI `/commodity-codes`: lista DataTableShell + dodanie + rozwiązanie tokenu

## Poza zakresem

TARIC live, towary niebezpieczne (Q6), osobna tabela aliasów, UN z M-52.

## HC

- RLS FORCE + test izolacji
- Kwoty nie mieszkają na katalogu
- LLM nie liczy
- ExtractionService nie importuje commodity_codes

## 70.0 HS/CN na RFQ i wycenie

Nullable `commodity_code_id` na `customer_rfq` i `quotation`. API składa katalog. Kwota wyceny nadal ze stawki. `/mail` Podpnij HS. `/quotations` picker. UN z M-52 leftover.
