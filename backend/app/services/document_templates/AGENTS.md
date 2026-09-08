# BC document_template (D9)

Szablon wydruku per tenant. Layout jako dane. Nie PDF, nie 409, nie etykieta sieci.

## Dozwolone zależności
- `app.models.document_template`
- `app.repositories.document_templates`
- `app.domain`

## Zakaz
- import innych BC services (shipments, charges, networks, quotations)
- zapis `shipment` / `charge` / `network` / `quotation`
- kwoty / marża / float / bajty PDF
- HTTP / ZPL / C8
