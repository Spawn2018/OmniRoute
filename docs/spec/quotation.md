# M-21 quotation — silnik wyceny SQL

**Plaster:** 2.0 fundament · **5.1** POL/POD + `party_id` (delta `docs/deltas/open/5.1-quotation-port-party.md`)  
**Status:** fundament + snapshot portu i kontrahenta. Kwota ze stawki. Nie marża. Nie k6. Nie `party_charge_override`.

## Zakres

- Tabela `quotation`: snapshot `organization_id`, `charge_code`, `rate_line_id`, `amount` Numeric(14,4) + `currency` CHAR(3), `source_ref`, `origin_port_id` (POL), `destination_port_id` (POD), `party_id`, timestamps
- INSERT…SELECT z `rate_line` gdzie `superseded_by IS NULL`; kwota tylko ze stawki, nigdy z requestu / LLM / Pythona
- Port i kontrahent nie dobierają stawki — UUID z requestu, FK złożone do `port` / `party`
- Nowa wycena: trójka POL+POD+`party_id` obowiązkowa (CHECK: wszystkie NULL albo wszystkie NOT NULL)
- Lista z filtrami SQL po trójce
- Brak bieżącej stawki = `quotation_gap` (luka wyceny)
- `charge_code` z katalogu 1.0; nie luźny string
- OpenFGA `can_manage_quotations` = member
- UI `/quotations`: lista DataTableShell + wycena po kodzie opłaty, kontrahencie i parze portów

## Poza zakresem

`charge` / `margin()`, `party_charge_override` w doborze kwoty, kolumny na `rate_line`, accept HITL, outbox, k6, Wave FE claim, druga tabela marży.

## HC

- RLS FORCE + test izolacji
- HC-02: Decimal + ISO; LLM nie liczy
- HC-07: dobór stawki w SQL, nie ORM na 50k wierszy
- ExtractionService nie importuje quotations / rates / parties
