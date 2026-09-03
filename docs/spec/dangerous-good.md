# M-52 dangerous_good — katalog towarów niebezpiecznych

**Plaster:** 7.0 (katalog) · **122.0** (S7 leftover UN na RFQ)  
**Status:** katalog numeru UN + klasy IMDG per tenant. 122.0 podpina `dangerous_good_id` do RFQ i wyceny. Nie żywe M-08 `charge`.

Delta: [7.0](../deltas/archived/7.0-dangerous-good.md) · [122.0](../deltas/archived/122.0-un-on-rfq.md).

## Zakres

- Tabela `dangerous_good`: `organization_id`, `un_number` (4 cyfry), `imdg_class` (allowlista IMDG), `name`, `aliases[]`, `source_ref`, timestamps
- Unikalność `(organization_id, un_number)`
- `resolve(token)` — numer UN albo alias; nieznany = `UnknownDangerousGood`
- OpenFGA `can_manage_dangerous_goods` = member
- UI `/dangerous-goods`: lista DataTableShell + dodanie + rozwiązanie tokenu

## Poza zakresem

`quotation` / `commodity_code` z FK w 7.0 · ADN/ADR jako osobne tabele · grupy zgodności 1.xA · packing group · live IMO · nadpisanie M-08 `charge`

## 122.0 UN na RFQ i wycenie

### Zakres

- Nullable `dangerous_good_id` na `customer_rfq` i `quotation`
- API składa katalog. Kwota wyceny nadal ze stawki. `/mail` Podpnij UN.

### Poza 122.0

Live IMO · LLM nadaje UN · filtr `rate_line` po UN

## HC

- RLS FORCE + test izolacji
- Kwoty nie mieszkają na katalogu
- LLM nie liczy i nie nadaje klasy IMDG
- ExtractionService nie importuje `dangerous_goods`
