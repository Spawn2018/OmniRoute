# Karty pól — Fala O (biurko wyceny morskiej) — SZKIC do `/plan-modul`

**Status:** szkic wejściowy. Finalne nazwy kolumn ustala Plan modułu wg `docs/GLOSSARY.md`. Każda tabela: `organization_id` + RLS FORCE + test izolacji. Kwoty `Numeric(14,4)` + `CHAR(3)`. LLM nie liczy rankingu, TT ani znaczków. API składa BC — serwis `carrier_inquiries` nie importuje `quotations`.  
**Kanon kolejki:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Fala O. Nie M-51 `ocean_lcl` (odcinek zlecenia). Nie live HTTP S21.  
**Wzorce trwałości:** jak [karty-pol-fala-t.md](karty-pol-fala-t.md) (słownik / szablon / M-03 / `table_view`).

Job operatora: na `/quotations` widzi oferty na lane, znaczniki najtańsza / najszybszy TT, dopisuje brakującą stawkę, zaznacza jednego / wielu / wszystkich agentów (domyślnie N najlepszych), czyta podpowiedź z historii pracy każdego wiersza, wysyła świadomie po S11.

## M-03 — klucze (nie kolumny)

| Klucz | Typ w `setting_value` | Domyślna | Uwagi |
|---|---|---|---|
| `ocean_inquiry_default_n` | int jako tekst | `3` | ile checkboxów zaznaczonych na starcie; max 8 |
| `ocean_inquiry_rank_max` | int jako tekst | `8` | sufit listy rankingu (wzorzec FV F10) |
| `ocean_scorecard_window_days` | int jako tekst | `90` | okno SQL karty lane |

## O0 — `network_member.party_id`

Tabela ISTNIEJE (82.0). Brak FK do `party` = nie da się liczyć zleceń / najtańszych na lane.

| Pole | Typ | Słownik / walidacja | Uwagi |
|---|---|---|---|
| `party_id` | UUID FK tenanta → `party` | nullable na starych wierszach | nowy członek: NOT NULL. Ranking/wysyłka bez wiązania = 409 „powiąż z kontrahentem” |
| `member_code` / `legal_name` | ISTNIEJE | — | nie duplikować nazwy kontrahenta po O0 |

## M10-1 / M10-2 (przed O4/O5)

| Pole | Typ | Uwagi |
|---|---|---|
| znormalizowany `tax_id` / `vat_eu` / EORI / DUNS | text + unique (org, token) | duplikat = 409 z linkiem; brak ID biznesowego = odmowa zapisu |
| `party_role` | tabela `party_role_assignment`: `party_id` + enum `customer` \| `vendor` \| `agent` \| `carrier` \| `subcontractor` \| … | wiele ról na jednym `party` |
| `is_sole_trader` | bool | JDG → kredyt tylko HITL |
| `parent_party_id` | UUID FK nullable | grupa / oddział / inny płatnik |

## B0a — `entity_event`

Append-only. Kind na Fali O: `inquiry_queued` / `inquiry_sent` / `quote_recorded`. `prediction_ledger` = B0b po T2.

| Pole | Typ | Uwagi |
|---|---|---|
| `subject_kind` | text | `carrier_inquiry` / `quotation` / `channel_quote` / … |
| `subject_id` | UUID | obiekt w tenancie |
| `event_kind` | text | allowlista w Plan O3 |
| `occurred_at` | timestamptz | |
| `source_ref` | text | obowiązkowe |

## O1 — `channel_quote.transit_days` + znaczki

Tabela ISTNIEJE (13.0): `amount`, `currency`, `quote_date`, POL/POD, `party_id`.

| Pole | Typ | Uwagi |
|---|---|---|
| `transit_days` | int ≥ 1, nullable na starych | dni kalendarzowe; brak = brak znaczka „najszybszy TT” |
| `is_cheapest` | nie kolumna | SQL w M-31: min `amount` w tej samej walucie na lane+dzień |
| `is_fastest_tt` | nie kolumna | SQL: min `transit_days` tam, gdzie NOT NULL, ta sama waluta |
| waluty mieszane | — | znaczek **w grupie waluty**; przeliczenie NBP = T7, nie ten plaster |

## O2 — ręczny wpis stawki z `/quotations`

POST istniejącego katalogu. `source_ref = tenant:manual:{user_id}`. Unikat dnia (org, party, POL, POD, quote_date) = 409. Nie mutacja kwoty. Wejście na `rate_line` / `charge` = 1.3, nie ten plaster.

## O3 — `carrier_inquiry` batch

Tabela ISTNIEJE (83.0): tylko `draft`, FK `network_member`, zero kwoty, zero lane.

| Pole | Typ | Uwagi |
|---|---|---|
| `status` | enum `draft` \| `queued` \| `sent` \| `answered` \| `declined` | CHECK; nie tylko `draft` |
| `origin_port_id` / `destination_port_id` | UUID FK → `port` | lane jak wycena |
| `quotation_id` | nie kolumna w serwisie buy | API składa odczyt wyceny; serwis nie importuje `quotations` |
| `quoted_amount` / `quoted_currency` | Numeric + CHAR(3) | tylko przy `answered` |
| `quoted_transit_days` | int nullable | przy `answered` |
| `sent_at` | timestamptz nullable | start pomiaru odpowiedzi |
| `answered_at` | timestamptz nullable | mediana godzin = SQL |

Batch POST: lista `network_member_id` (z `party_id`). „Wszyscy” = filtr M-03 (sieć + rola agent/carrier), nie scraping.

## O4 — zaznaczenie i szkice

**138.0 zamknięty `/noc`:** ta sama `mail_draft` + `inquiry_default_n` + ranking SQL `answered`. Nie O5.

| Pole / zachowanie | Typ | Uwagi |
|---|---|---|
| checkboxy | UI | nic / jeden / wielu / wszyscy |
| default N | M-03 | SQL ranking, nie model |
| ranking | okno SQL | waga: zlecenia na POL/POD, `median_response_hours`, `cheapest_count`, świeżość, kara `sample_size=0` |
| `mail_draft` | N wierszy albo jeden z wieloma `To` | rozstrzyga Plan O4; Graph HTTP leftover; send = S18 `mailto:` po S11; zakaz auto-send |

## O5 — `party_lane_scorecard`

Nowa tabela. Pogłębienie M-13, nie scoring osoby, nie karta globalna zamiast lane.

| Pole | Typ | Uwagi |
|---|---|---|
| `party_id` | UUID FK | agent / armator / podwykonawca |
| `origin_port_id` / `destination_port_id` | UUID FK → `port` | lane |
| `window_days` | int | z M-03 |
| `sample_size` | int ≥ 0 | 0 = nadal jest wiersz UI |
| `median_response_hours` | Numeric nullable | SQL z `sent_at`/`answered_at` |
| `shipment_count` | int | zlecenia z tym `party` na lane w oknie |
| `cheapest_count` | int | ile razy `channel_quote` był min na lane |
| `answered_inquiry_count` | int | |
| `computed_at` | timestamptz | |
| `source_ref` | text | `sql:refresh:{batch}` |

Tekst podpowiedzi = szablon z pól SQL (nie LLM). `sample_size=0`: „brak historii na tym kierunku — karta globalna / sieć”. Każdy wiersz listy ma tekst.

## O6 — `extraction_draft.draft_kind = carrier_quote`

Kolumna `draft_kind` w [pola-wizja-2026-09.md](pola-wizja-2026-09.md) §7.1 — dopisać wartość `carrier_quote`. Accept HITL → INSERT `channel_quote` + `carrier_inquiry.status=answered`. `ExtractionService` nie zapisuje stawek.

## O7 — kraj na liście (bez nowej kolumny)

`party.country_code` ISTNIEJE (ISO 3166-1 alpha-2). Lista O4: kolumna + filtr. Holandia na SHA→RTM = ten filtr. Nie druga kolumna kraju.

## O8 — widok wiadomości buy-desk

`table_view.group_by`: `party` \| `country` \| `thread` \| `status`. Default `party`. Wątek = `inbound_message.rfc822_message_id` / `in_reply_to`. Nie nowy czat. Audyt [incoterms-booking-customs-ux.md](incoterms-booking-customs-ux.md).

## Poza Falą O

Live Maersk/Hapag · S21 · 8 twinów PDF · auto-send · ranking w Pythonie na 50k · druga marża · M-51 LCL.
