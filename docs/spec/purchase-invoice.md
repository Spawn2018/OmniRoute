# purchase_invoice (F10)

HITL katalog faktury zakupu per tenant. Nie ranking. Nie allocation. Nie kwota.

## Zakres

- Tabela `purchase_invoice`: organization_id, invoice_ref, invoice_kind (`noted`|`other`), source_ref, created_at.
- RLS + unique (organization_id, invoice_ref).
- API GET/POST `/purchase-invoices`. OpenFGA `can_manage_purchase_invoices`.
- UI lista + formularz.
- Nie UPDATE/DELETE. Nie FK do charge. Nie kwota.

## Poza zakresem

- invoice_match_candidate / ranking SQL / purchase_invoice_allocation
- auto-link do charge / sales_invoice
- live ERP / KSeF XML
- charge / marża

## Zależności

- tenancy · F9 erp_connector (klej poza tym plastrem)
