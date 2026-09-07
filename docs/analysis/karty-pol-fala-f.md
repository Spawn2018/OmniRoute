# Karty pól — Fala F (finanse głębiej) — SZKIC do `/plan-modul`

**Kolizja ID:** ta fala używa **F1–F11** (bez kropki). Historyczne **F11.0** = M-68 obserwowalność (zamknięte). **F9.0** = M-57 copilot. **F9.1** = S56–S58. KSeF live = **F1** tutaj, nie S35 (numer sesji).  
**Pola:** [pola-wizja-2026-09.md](pola-wizja-2026-09.md) §6 ERP, §9 Poczta, §10 FV zakup + lejek. [erp-fk-adapter.md](erp-fk-adapter.md).

| ID | Tabele / pola | Uwagi |
|---|---|---|
| F1 | KSeF live FA(3), tryby, QR; `ksef_issuer=omni` | mandat PL 2026; nie KSeF z ERP |
| F2 | skonto / rezerwy / rozliczenia wewnętrzne | Decimal; nie druga marża |
| F3 | noty + period closing | |
| F4 | CAMT/MT940 + HITL rekoncyliacja; bramka biała lista przy przelewie | pogłębienie M-42 |
| F5 | delegacje / diety | TO_VERIFY stawki per kraj; nie LLM |
| F6 | windykacja; blokada `POST shipment` po limicie | pogłębienie M-14; szkic AI = M14b; zapis limitu tylko S11 |
| F7 | faktoring POD → wypłata | TO_VERIFY partner |
| F8 | Peppol | kalendarz UE; nie zastępuje KSeF |
| F9 | `purchase_invoice`; `erp_connector` / `erp_series_map` / `erp_export` | FS+FZ do FK; agent outbound; zakaz `sa`/SQL do MSSQL klienta |
| F10 | ingest FV: mail / KSeF XML / skan → `draft_kind=purchase_invoice` → `invoice_match_candidate` SQL → HITL | nigdy auto-link; XML bez LLM |
| F11 | `paper_post` → `postal_dispatch` + EN + REST USS + `postal_epo` | papier ≠ wyłączenie KSeF; imię tylko EPO; umowa PP TO_VERIFY |

P0 `charge.source_ref` musi być **przed** F11 (znaczek) i V2b (myto).
