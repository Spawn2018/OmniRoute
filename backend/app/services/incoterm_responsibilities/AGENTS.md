# BC incoterm_responsibility (I1)

Katalog macierzy obowiązków per tenant. Seed Omni ops. Nie cytat ICC. Nie booking.

## Dozwolone zależności
- `app.models.incoterm_responsibility`
- `app.repositories.incoterm_responsibilities`
- `app.domain`

## Zakaz
- import innych BC services (quotations, shipments, charges)
- zapis `quotation` / `shipment` / `charge`
- kwoty / marża / float
- HTTP / cytat ICC / LLM wybierający Incoterms
