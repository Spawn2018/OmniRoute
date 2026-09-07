# Karty pól — Fala I (Incoterms / booking / odprawa / buy-desk) — SZKIC

**Kanon:** PLAN § Fala I. Wzorzec maila = Fala O. LLM nie wybiera Incoterms ani adresata.  
**Audyt (TMS + nauka + UX):** [incoterms-booking-customs-ux.md](incoterms-booking-customs-ux.md).

## I1 — `incoterm_responsibility`

Katalog per tenant (seed z alokacji ICC 2020 jako dane Omni, `source_ref=omni:incoterms2020:ops`). Override tenanta = nowy wiersz.

| Pole | Typ | Uwagi |
|---|---|---|
| `incoterm` | enum 11 reguł 2020 | nie luźny string |
| `trade_side` | enum `import` \| `export` | kto jest klientem Omni |
| `export_clearance_role` | enum roli | `seller` / `buyer` / `omni_customs` / `origin_agent` / `client_customs` |
| `import_clearance_role` | enum roli | DDP → seller strona; reszta buyer |
| `main_carriage_booker` | enum | `seller` \| `buyer` |
| `booking_scope` | enum[] | `precarriage` / `ocean` / `oncarriage` / `contact_exchange` / `none` |
| `source_ref` | text | obowiązkowe |

## I2 — `shipment_stakeholder`

| Pole | Typ | Uwagi |
|---|---|---|
| `shipment_id` | FK | zlecenie ISTNIEJE |
| `role` | enum | `shipper` / `consignee` / `origin_agent` / `dest_agent` / `ocean_carrier` / `omni_customs` / `client_customs` |
| `party_id` | FK → `party` | 409 na dispatch bez party |
| `source_ref` | text | |

## I3 — reguła + wysyłka dokumentów

`document_dispatch_rule`: (`trade_side`, `incoterm`, `document_kind`) → `recipient_role`.  
`document_dispatch`: `shipment_id`, `party_id`, lista `shipment_document`, `mail_draft_id`, status `draft`/`sent`. Send = S18 po S11. Zakaz auto-send.

## I4 — `booking_instruction`

| Pole | Typ | Uwagi |
|---|---|---|
| `shipment_id` | FK | |
| `booking_scope` | enum | z I1 |
| `target_role` | enum | z I1; party z I2 |
| `status` | `suggested` / `accepted` / `sent` / `confirmed` / `rejected` | suggested = SQL; accept = człowiek |
| `source_ref` | text | |

DAP import + `contact_exchange`: dwa szkice (origin_agent, client) — nie booking armatora.

## O7 — kraj na liście (bez nowej kolumny)

`party.country_code` ISTNIEJE (ISO 3166-1 alpha-2). Lista zapytań O4: kolumna + filtr. Holandia na SHA→RTM = ten filtr.

## O8 — widok wiadomości

`table_view.group_by` (albo klucz M-03 + saved view): `party` \| `country` \| `thread` \| `status`. Default `party`. Wątek = `inbound_message.rfc822_message_id` / `in_reply_to` (pola-wizja). Nie nowy czat.
