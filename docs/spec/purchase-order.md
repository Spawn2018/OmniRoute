# purchase_order (CT1)

Katalog nagłówka zamówienia zakupu per tenant. HITL kod + opcjonalny zakład. Nie linia SKU. Nie ASN. Nie shipment.

- RLS FORCE. OpenFGA `can_manage_purchase_orders` = member
- `po_code`: snake 2–32
- `plant_label`: opcjonalny tekst 1–128 (etykieta, nie FK)
- Unique `(organization_id, po_code)` i `(organization_id, source_ref)`
- Katalog INSERT, bez UPDATE/DELETE
- ExtractionService nie importuje tego BC
- Job: `/purchase-orders`

Delta: [276.0](../deltas/archived/276.0-purchase-order.md).
