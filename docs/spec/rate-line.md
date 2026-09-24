# M-07 rate_line — stawka kupna

**Plaster:** **646.0** (zamknięty; 1.1 fundament)  
**Status:** fundament + EXP1 allotment TEU HITL. Nie `charge` buy+sell (1.2). Nie accept HITL → stawki (1.3).

Delta 646.0: [docs/deltas/archived/646.0-rate-line-allotment.md](../deltas/archived/646.0-rate-line-allotment.md).

## Zakres

- Tabela `rate_line`: `organization_id`, `charge_code` (token z katalogu 1.0), `amount` Numeric(14,4) + `currency` CHAR(3), `source_ref`, opcjonalny `allotment_teu` Numeric(14,4) (≥ 0, nullable), `superseded_by`, timestamps
- `source_ref` obowiązkowy; puste / sam whitespace = odrzut
- Kwota tylko przez `Money` (Decimal + ISO); JSON `amount` jako tekst, nie float
- `allotment_teu` opcjonalny HITL; bez pola → null; ujemny / float → 400; zmiana = supersede
- Zmiana = nowy wiersz + `superseded_by` na poprzedniku; trigger blokuje UPDATE kwoty/waluty/`source_ref`/`allotment_teu` i DELETE
- OpenFGA `can_manage_rate_lines` = member
- UI `/rate-lines`: lista DataTableShell + dodanie + zastąpienie

## Poza zakresem

`charge` / marża (1.2), accept HITL → RatesService (1.3), spot_or_contract / index_id FSC, matching, outbox, Wave FE U-*.

## HC

- RLS FORCE + test izolacji
- HC-02: nigdy float; LLM nie liczy
- HC-03: bez `source_ref` stawka nie wchodzi; niemutowalność
