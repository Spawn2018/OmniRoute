# BC sap_connector (CT6)

HITL katalog konektora SAP/Oracle per tenant. connector_code + system_kind `sap`|`oracle` + source_ref. Nie live SOAP. Nie sekrety. Nie SQL do SAP.

## Dozwolone zależności
- `app.models.sap_connector`
- `app.repositories.sap_connectors`
- `app.domain`

## Zakaz
- import innych BC services (erp_connectors, charges, sales_invoices, bookkeeping, extraction)
- zapis `erp_connector` / `charge` / `sales_invoice` / `bookkeeping`
- live SOAP / RFC / SQL `sa` / kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- kolumny sekretu / ciphertext / `api_key` / `base_url`
