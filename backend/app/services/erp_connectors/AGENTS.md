# BC erp_connector (F9)

HITL katalog konektora Comarch Optima per tenant. connector_code + system_kind `optima` + source_ref. Nie live SOAP. Nie sekrety.

## Dozwolone zależności
- `app.models.erp_connector`
- `app.repositories.erp_connectors`
- `app.domain`

## Zakaz
- import innych BC services (charges, sales_invoices, bookkeeping, parties, extraction)
- zapis `charge` / `sales_invoice` / `bookkeeping` / `party` / `purchase_invoice`
- SQL `sa` / SOAP / WebAPI / kwota / marża / float
- HTTP / XL / nexo / GT / Symfonia / KSeF / CAMT
- UPDATE / DELETE wiersza
- kolumny sekretu / ciphertext / `base_url`
