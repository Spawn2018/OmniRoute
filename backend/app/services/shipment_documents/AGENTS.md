# BC shipment_document (M-38)

Wskazanie dokumentu per tenant, FK do `shipment`. 624.0 rodzaj `rod`. Nie bajty, nie numer listu, nie skan M-20. Nie token `pod`.

## Dozwolone zależności
- `app.models.shipment_document`
- `app.repositories.shipment_documents`
- `app.domain`

## Zakaz
- import innych BC services (shipments, quotations, extraction)
- zapis `shipment` / `quotation` / `charge` / `extraction_draft`
- kwoty / marża / float / bajty pliku
- HTTP / treść przez LLM
