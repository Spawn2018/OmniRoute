# BC sales_invoice (M-40)

Faktura sprzedaży per tenant, FK do `shipment`. Numer sesji KSeF to pole na wierszu.
Nie live HTTP, nie XML, nie kwota, nie druga marża.

## Dozwolone zależności
- `app.models.sales_invoice`
- `app.repositories.sales_invoices`
- `app.domain`

## Zakaz
- import innych BC services (shipments, charges, quotations)
- zapis `shipment` / `charge` / `quotation`
- kwoty / marża / float
- HTTP / httpx / XML / FA(3)
