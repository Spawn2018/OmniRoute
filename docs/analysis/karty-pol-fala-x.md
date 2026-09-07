# Karty pól — Fala X (portale / mobile / mapa / skan) — SZKIC do `/plan-modul`

**Kanon:** po Auth0 **S53**. `/noc` nie startuje X1/X2 bez IdP.  
**Pola:** [pola-wizja-2026-09.md](pola-wizja-2026-09.md) §5 mapy, §7 HITL/skan, §10.3–10.5 lejek.

| ID | Tabele / pola | Uwagi |
|---|---|---|
| X1 | portal klienta: odczyt `shipment` / T&T / `shipment_document` | Auth0; nie atrapa JWT hello |
| X2 | portal przewoźnika: `trip`, taski, POD, self-billing | po T2/T5 |
| X3 | apka kierowcy = GPS L0 na czas `trip` | zgoda; flota 24/7 tylko `omni_telematic` + umowa (V5) |
| X4 | konsument `outbox_event` + webhook outbound | pierwszy realny konsument; warunek S59 |
| X5 | API OAuth2 portal ≠ tenant | OpenAPI wewnętrzne już jest |
| X6 | diff ePOD/CMR vs zlecenie: zgodne/konflikt/nowe | po X9; HITL zostaje |
| X7 | `quote_engagement` (`sent`/`pdf_viewed`/`delivered`/`lost`/…); `quote_view_token`; czasy SQL | piksel tylko po `tracking_consent`; mailto bez Graph = link PDF |
| X8 | `map_basemap`; `user_map_prefs`; `tenant_map_provider` (ciphertext) | zakaz `tile.openstreetmap.org`; OpenFreeMap/GUGiK P0 |
| X9 | `scan_enhance_run`; bbox/pewność w payload; `draft_kind`; split ui-04 | OpenCV+ML Kit/VisionKit; zakaz GAN; optimistic accept zakazany |

M-03: `hitl_confidence_green` / `hitl_confidence_amber` (pola-wizja §1.2).
