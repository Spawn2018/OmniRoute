# Karty pól — Fala D (drobnica / LTL) — SZKIC do `/plan-modul`

**Kanon:** [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) po T1–T2 (`stop` na sieci). Nie pełny WMS. Nie optymalizator.  
**Pola szczegółowe:** [pola-wizja-2026-09.md](pola-wizja-2026-09.md) §8 (wydruk/QR), T1 w [karty-pol-fala-t.md](karty-pol-fala-t.md).

| ID | Tabele / pola (szkic) | Poza zakresem |
|---|---|---|
| D1 | linia: cutoff, `transit_days`, dni operacyjne; FK `location` | OR lokalizacji hubów |
| D2 | `shipment_package` + statusy 4 poziomów; skan kodu; walidacja wg trasy | auto-link bez QR Omni |
| D3 | cross-dock / magazyn spedycyjny + awizacja na `stop` | WMS e-commerce |
| D4 | COD; POD/ROD jako `shipment_document` | rozliczenie pobrań = Fala F |
| D5 | cennik strefa/waga/objętość/paleta + FSC | silnik = P1; nie T-SQL |
| D6 | konsolidacja LCL; HBL/MBL; pule numerów (M-03 szablon) | booking armatorski (HZ/S21) |
| D7 | saldo palet per `party` | giełda palet |
| D8 | etykieta sieci po **oficjalnym** API | TO_VERIFY; udawany generator = odrzut |
| D9 | `document_template`; `network_print_requirement` (409 bez wydruku); QR `shipment_ref`; skan zwrotny | bez kodu Omni = HITL |

`shipment_ref` na `shipment` — obowiązkowy przed D9/F10 (profilaktyka FV).
