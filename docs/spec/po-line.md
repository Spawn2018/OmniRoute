# po_line (CT1)

Katalog linii zamówienia zakupu per tenant. HITL SKU + qty Decimal + JM. Nie ASN. Nie shipment.

- RLS FORCE. OpenFGA `can_manage_purchase_orders` = member (ta sama relacja co 276.0)
- `line_code`: snake 2–32
- `purchase_order_id`: złożone FK do `purchase_order` w tym samym BC
- `qty`: Numeric(14,4) ≥ 0, nie float
- Unique `(organization_id, purchase_order_id, line_code)` i `(organization_id, source_ref)`
- Katalog INSERT, bez UPDATE/DELETE
- ExtractionService nie importuje tego modelu
- Job: `/po-lines`

Delta: [277.0](../deltas/archived/277.0-po-line.md).
