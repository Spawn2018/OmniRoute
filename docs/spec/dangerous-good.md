# M-52 dangerous_good — katalog towarów niebezpiecznych

**Plaster:** 7.0 (katalog) · **122.0** (UN na RFQ) · **192.0** (tunel ADR + SG) · **642.0** (packing group) · **643.0** (marine pollutant) · **644.0** (limited quantity)  
**Status:** katalog numeru UN + klasy IMDG + tunel ADR + grupa SG + packing group I/II/III + MP + LQ per tenant. Nie żywe M-08 `charge`. LLM nie nadaje klasy.

Delta: [7.0](../deltas/archived/7.0-dangerous-good.md) · [122.0](../deltas/archived/122.0-un-on-rfq.md) · [192.0](../deltas/archived/192.0-dangerous-good-adr.md) · [642.0](../deltas/archived/642.0-dangerous-good-packing-group.md) · [643.0](../deltas/archived/643.0-dangerous-good-marine-pollutant.md) · [644.0](../deltas/archived/644.0-dangerous-good-limited-quantity.md).

## Zakres

- Tabela `dangerous_good`: `organization_id`, `un_number` (4 cyfry), `imdg_class` (allowlista IMDG), `name`, `aliases[]`, `source_ref`, timestamps
- Unikalność `(organization_id, un_number)`
- `resolve(token)` — numer UN albo alias; nieznany = `UnknownDangerousGood`
- OpenFGA `can_manage_dangerous_goods` = member
- UI `/dangerous-goods`: lista DataTableShell + dodanie + rozwiązanie tokenu

## Poza zakresem

`quotation` / `commodity_code` z FK w 7.0 · ADN/ADR jako osobne tabele · grupy zgodności 1.xA · live IMO · nadpisanie M-08 `charge`

## 122.0 UN na RFQ i wycenie

### Zakres

- Nullable `dangerous_good_id` na `customer_rfq` i `quotation`
- API składa katalog. Kwota wyceny nadal ze stawki. `/mail` Podpnij UN.

### Poza 122.0

Live IMO · LLM nadaje UN · filtr `rate_line` po UN · packing group · grupy 1.xA

## 192.0 tunel ADR + grupa SG

### Zakres

- `adr_tunnel_code`: `A` | `B` | `C` | `D` | `E`
- `segregation_group`: `none` | `sg1`…`sg18`
- Operator wpisuje kody; serwis nie zmienia `imdg_class`

### Poza 192.0

packing group · live IMO · LLM klasa

## 642.0 packing group

### Zakres

- `packing_group`: `I` | `II` | `III` (HITL; NOT NULL; CHECK w bazie; backfill `II`)
- Operator wpisuje grupę; serwis nie zmienia `imdg_class` / ADR / SG
- UI: kolumna + select przy dodaniu

### Poza 642.0

live IMO · LLM klasa · grupy zgodności 1.xA · nowy BC mark

## 643.0 marine pollutant

### Zakres

- `marine_pollutant`: bool HITL (NOT NULL; backfill `false`)
- Operator zaznacza MP; serwis nie zmienia `imdg_class`
- UI: kolumna + checkbox

### Poza 643.0

live IMO · LLM klasa · grupy 1.xA · LQ

## 644.0 limited quantity

### Zakres

- `limited_quantity`: bool HITL (NOT NULL; backfill `false`)
- Operator zaznacza LQ; serwis nie zmienia `imdg_class`
- UI: kolumna + checkbox

### Poza 644.0

live IMO · LLM klasa · grupy 1.xA

## HC

- RLS FORCE + test izolacji
- Kwoty nie mieszkają na katalogu
- LLM nie liczy i nie nadaje klasy IMDG
- ExtractionService nie importuje `dangerous_goods`
