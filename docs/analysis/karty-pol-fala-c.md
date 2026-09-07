# Karty pól — Fala C (celna / compliance) — SZKIC do `/plan-modul`

**Kanon:** po T2 tam, gdzie brama na `POST shipment`. Nie scoring osoby. Brak klona SENT w kraju ≠ wymyślony adapter.  
**Pola:** [pola-wizja-2026-09.md](pola-wizja-2026-09.md) §1.3, §4.

| ID | Tabele / pola | Uwagi |
|---|---|---|
| C1 | SENT + SENT-GEO (PUESC); `shipment_monitoring_filing` | XML/XSD; nie „SENT-Europa” |
| C2 | AIS-IMPORT / AES / Intrastat | TO_VERIFY konto PUESC |
| C3 | Biała lista / VIES / GUS live | pogłębienie lookup M-10; szkic, nie auto-zapis `party` |
| C4 | eCMR / eFTI | cel 2027; nie Selenium |
| C5 | CO₂ GLEC/GHG: metodologia + wersja + `source_ref` | nie jedna uniwersalna liczba |
| C6 | BDO/KPO; DIWASS/WSR; `shipment.is_waste` | API MOS; zmiana 1.01.2027 |
| C7 | `monitoring_scheme` katalog per tenant | tylko ze źródłem prawnym (EKAER, e-Transport, …) |
| C8 | `party_document`; `relation_document_requirement`; 409 na `POST shipment` | odblokowanie = nowy wiersz dokumentu; HITL extract |
| C9 | `party_exchange_snapshot` (Trans.eu partners-api) | zakaz scrapingu opinii; próg blokady = M-03 |
