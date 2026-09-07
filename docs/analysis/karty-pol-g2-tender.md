# Karty pól — G2 Tender desk Enterprise

**Kanon:** PLAN § G2. P6 ≠ G2. Pin 2026-09-08c.

## `tender`

| Pole | Uwagi |
|---|---|
| `side` | sell \| buy |
| `kind` | open \| restricted \| sealed \| e_auction |
| `status` | draft…awarded \| lost \| no_bid |
| `buyer_party_id` | |
| `deadline_at` | kalendarz U4 |
| `incoterm` + `trade_side` + `named_place` | |
| `source_ref` | |

Dalej: `tender_lot`, `tender_lane`, `tender_round`, `tender_data_room` (OpenFGA+NDA), `tender_matrix_cell` (kwota z P, nie z LLM), `tender_playbook` (każde twierdzenie + source_ref), `win_loss`.

## G2.19–G2.22

`lane_pattern` z actuals. `circle_sim` ≥500k w Postgres (nie Python). Constraint: unload A ∩ load B. Km ładowny / pusty / dolot Decimal. P = n_overlap/n_similar; brak historii ≠ 87%. Copy „natychmiast” dopiero po p95 na stage.

## G2.23 KREPTD

Portal [kreptd.gitd.gov.pl](https://kreptd.gitd.gov.pl/). API Citizen: certyfikat `api.kreptd@gitd.gov.pl`, 120/h. Szkic `party` + `party_document` kind=`transport_licence`. Pola: `kreptd_licence_no`, `kreptd_checked_at`. Zakaz scrape HTML.
