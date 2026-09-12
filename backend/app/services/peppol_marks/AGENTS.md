# BC peppol_mark (EXP2.20)

HITL katalog znacznika Peppol/MPP per tenant. mark_code + peppol_kind
peppol|mpp|as4|other + source_ref. Nie AS4 HTTP. Nie live.
Obok `sales_invoice` — tu kanał e-faktury, nie KSeF XML.

## Dozwolone zależności
- `app.models.peppol_mark`
- `app.repositories.peppol_marks`
- `app.domain`

## Zakaz
- import innych BC services (sales_invoices, charges, extraction, erp_connectors)
- zapis `sales_invoice` / `charge` / `extraction_draft`
- Peppol live · AS4 HTTP · MPP poll · bajty
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
