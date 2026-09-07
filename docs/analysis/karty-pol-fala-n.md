# Karty pól — Fala N (nauka / ops)

**Kanon:** PLAN. Klej — nie osobny produkt. Pin 2026-09-08c.

| ID | Obiekt / pole | Gdzie w osi |
|---|---|---|
| N1 | `consignment` (shipment 1→N) | po T1, przed D2 |
| N2 | `trips_to_bill` | po T2+F1 |
| N3 | zegar D&D (free days → countdown + szkic charge) | z V3 |
| N4 | godziny `terminal` + cutoff | z T8 |
| N5 | `no_reply_after` + notice | po O8 |
| N6 | `margin_floor` Decimal | po P0+P1 |
| N7 | ETA przedział + kalibracja ledger | z V1/V2 |
| N8 | koalescencja alertów | z W2 |
| N9 | F2 + klon podobnego zlecenia | z U1 |
| N10 | board klawiatura / Fitts / wirtualizacja | z T6 |
| N11 | handover SBAR | po T6 |
| N12 | macierz VAT jako dane | z F1 |
| N13 | period lock | z F3 |
| N14 | self-billing | po F9+D |
| N15 | szablony mail EN | z O4 |
| N16 | sandbox + seed słowników | po katalogach |
| N17 | `party.channel_pref` email/whatsapp/mailto | z WA1 |

Zakaz: LLM-VRP, auto-assign bez S11, ETA punkt bez ledger.
