# Karty pól — Fala CT (wieża załadowcy / 4PL)

**Kanon:** PLAN § Fala CT. Tenant shipper RLS. Pin 2026-09-08c.

| ID | Pola / obiekty | Zakaz |
|---|---|---|
| CT1 | `purchase_order`, `po_line` (sku, qty, uom, plant, batch, serial, coo), ASN | |
| CT2 | łańcuch V6; bez CI = „brak danych umowy” | auto stop produkcji |
| CT3 | OTIF pickup / delivery / SKU | |
| CT4 | `routing_guide` → 409 | |
| CT5 | EDI 214/315/856/210 | scrape |
| CT6 | erp_connector SAP | SQL do SAP |
| CT7 | visibility vendor capability | drugi vendor naraz jako prawda |
| CT8 | port_congestion + AIS leftover | bez licencji |
| CT9 | GLEC + methodology_version | |
| CT10 | expected charge vs FV | druga marża |
| CT11 | role OpenFGA 3 strony | cross-shipper SELECT |
| CT12 | capa, 8d, recurrence | |
