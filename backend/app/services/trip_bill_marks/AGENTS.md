# BC trip_bill_mark (N2)

HITL katalog znacznika gotowości przejazdu do FV per tenant. mark_code +
bill_kind ready|held|billed|other + source_ref.
Nie SQL trips_to_bill. Nie F1 KSeF live.

## Dozwolone zależności
- `app.models.trip_bill_mark`
- `app.repositories.trip_bill_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, sales_invoices, collective_invoices, charges, extraction)
- zapis `trip` / `sales_invoice` / `collective_invoice` / `charge` / `extraction_draft`
- SQL trips_to_bill · F1 KSeF live · auto FV · FK trip/sales_invoice
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
