# BC collective_invoice (M-91)

Zbiorcza faktura per tenant. Wiąże `sales_invoice` z dodatkowym `shipment`.
Nie kwota, nie JPK, nie płatność paczką, nie live HTTP.

## Dozwolone zależności
- `app.models.collective_invoice`
- `app.repositories.collective_invoices`
- `app.domain`

## Zakaz
- import innych BC services (sales_invoices, shipments, charges)
- zapis `sales_invoice` / `shipment`
- kwoty / marża / float / suma
- HTTP
