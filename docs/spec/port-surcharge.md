# M-18 port_surcharge — opłaty portowe warunkowe

**Moduł żywy:** M-18 (archiwum M-18; nie koliduje z żywym M-08 `charge` / M-07 `rate_line`)  
**Plaster:** **12.0** katalog · **69.0** matching `applies_when`  
**Status:** katalog extra per `port` + ewaluacja warunku w SQL. Nie zapis do `charge`.

Delta: [docs/deltas/archived/12.0-port-surcharge.md](../deltas/archived/12.0-port-surcharge.md).

## 12.0 katalog extra portowego

### Zakres

- Tabela `port_surcharge` per tenant: `organization_id`, `port_id`, `code` (snake), `title`, `applies_when` (tekst warunku — dane, nie parser), `amount` Numeric(14,4) + `currency` CHAR(3), `source_ref`, timestamps
- Unikat `(organization_id, port_id, code)`. FK złożone do `port`
- `resolve(port_id, code)` dokładne po kodzie
- OpenFGA `can_manage_geography` = member (przy porcie, nie przy marży)
- UI `/port-surcharges` + panel na `/ports`

### Poza 12.0

Ewaluacja `applies_when` (69.0) · zapis do `charge` / `rate_line` · THC live z terminalu · M-19 kanały · ExtractionService · LLM liczący kwotę

## 69.0 matching `applies_when`

`GET /port-surcharges/matching` — SQL `port_id` + równość znormalizowanego `applies_when`. Nie parser AST. Nie INSERT `charge`. UI „Dopasuj warunek” na `/port-surcharges`.

### HC

- RLS FORCE + test izolacji
- `charge` zostaje jedynym miejscem prawdy o marży — tu jest katalog extra, nie buy+sell
- Kwota Decimal, waluta nierozerwalnie; nigdy float
- ExtractionService nie importuje `port_surcharges` / `charges` / `rate_lines`
- LLM nie liczy
