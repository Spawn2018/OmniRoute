# M-23 nbp_rate — katalog kursu NBP

**Plaster:** 6.0 (delta `docs/deltas/archived/6.0-nbp-rate.md`)  
**Status:** katalog kursu średniego tabeli A per tenant. Nie przeliczenie wyceny. Nie żywe M-07 `rate_line`.

## Zakres

- Tabela `nbp_rate`: `organization_id`, `currency` (ISO 4217), `rate_date`, `mid` (`Numeric(14,4)`), `source_ref`, timestamps
- Unikalność `(organization_id, currency, rate_date)`
- `resolve(currency, on_date)` — najnowszy `rate_date <= on_date` (D-1 z tabeli NBP, nie kalendarz w Pythonie)
- OpenFGA `can_manage_nbp_rates` = member
- UI `/nbp-rates`: lista DataTableShell + dodanie z `source_ref` = `tenant:manual`; ingest fixture (nie live HTTP w CI)

## Poza zakresem

Przeliczanie `quotation` / `charge` / `rate_line` · tabela C kupno/sprzedaż · ECB · kalendarz świąt PL · Fala 3 „Waluty w ofercie” · nadpisanie M-07 `rate_line`

## HC

- RLS FORCE + test izolacji
- Kwota kursu = `Decimal` / `Numeric(14,4)`, nigdy float
- LLM nie liczy i nie woła NBP
- ExtractionService nie importuje `nbp_rates`
