# M-07 rate_line — stawka kupna

**Plaster:** **647.0** (zamknięty; 646.0 allotment; 1.1 fundament)  
**Status:** fundament + EXP1 allotment TEU + spot_or_contract HITL. Nie `charge` buy+sell (1.2). Nie accept HITL → stawki (1.3).

Delta 647.0: [docs/deltas/archived/647.0-rate-line-spot-contract.md](../deltas/archived/647.0-rate-line-spot-contract.md).

## Zakres

- Tabela `rate_line`: `organization_id`, `charge_code`, `amount` Numeric(14,4) + `currency` CHAR(3), `source_ref`, opcjonalny `allotment_teu`, opcjonalny `spot_or_contract` (`spot`|`contract`|`other`), `superseded_by`, timestamps
- `source_ref` obowiązkowy; puste / sam whitespace = odrzut
- Kwota tylko przez `Money` (Decimal + ISO); JSON `amount` jako tekst, nie float
- `allotment_teu` / `spot_or_contract` opcjonalne HITL; bez pola → null; zmiana = supersede
- Trigger blokuje UPDATE kwoty/waluty/`source_ref`/`allotment_teu`/`spot_or_contract` i DELETE
- OpenFGA `can_manage_rate_lines` = member
- UI `/rate-lines`: lista DataTableShell + dodanie + zastąpienie

## Poza zakresem

`charge` / marża (1.2), accept HITL → RatesService (1.3), index_id FSC, matching, outbox, Wave FE U-*.

## HC

- RLS FORCE + test izolacji
- HC-02: nigdy float; LLM nie liczy
- HC-03: bez `source_ref` stawka nie wchodzi; niemutowalność
