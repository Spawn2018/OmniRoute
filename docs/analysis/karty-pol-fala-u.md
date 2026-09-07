# Karty pól — Fala U (klej oferty / kalendarz / air / UI)

**Kanon:** PLAN § Fala U. Pin 2026-09-08c. U6 nie jest plasterem — DoD każdego UI.

## I0 / U2 — Incoterms na `quotation`

| Pole | Typ | Uwagi |
|---|---|---|
| `incoterm` | enum 11 | nie luźny string |
| `incoterms_version` | enum `2020`/`2010` | EXP0.6 |
| `named_place` | text | 409 na DAP/DDP bez miejsca |
| `trade_side` | `import`/`export` | |

## U1 — carry-forward

Mapa danych (nie kod): quotation → shipment → booking/dispatch → invoice. Klucze: incoterm, side, POL/POD, HS, wagi, stakeholderzy, refs, waluta. Diff przy POST. Mutacja = nowy wiersz / `superseded_by`.

## U3 — air

`shipment_leg.kind += air`. HAWB/MAWB, pule M-03. Lotnisko = `port` z flagą air. e-rates = `channel_quote`+`source_ref`.

## U4 — `organization_calendar`

Dni robocze + święta per `country_code`. SQL `is_working_day`. Grace V5 = 3 wywołania, nie +3 kalendarz.

## U5 — `document_checklist_rule`

`(incoterm, trade_side, mode)` → `document_kind` + `blocks_dispatch`. ≠ C8.

## U6 + M-72

Pola z karty, puste, 409 PL, job-metric, axe. Zakaz lista UUID.
