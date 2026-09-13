# BC factoring_connector (BR5.0)

HITL katalog konektora faktoringu per tenant. connector_code + system_kind `smeo|other` + source_ref. Nie live SMEO HTTP. Nie sekrety. Nie workflow wypłaty.

## Dozwolone zależności
- `app.models.factoring_connector`
- `app.repositories.factoring_connectors`
- `app.domain`

## Zakaz
- import innych BC services (sales_invoices, bank_payments, cash_flows, working_capital_marks, charges, extraction)
- zapis `sales_invoice` / `bank_payment` / `cash_flow` / `charge` / `extraction_draft`
- live SMEO HTTP / OAuth / webhook wypłaty / kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- kolumny sekretu / ciphertext / `base_url`
