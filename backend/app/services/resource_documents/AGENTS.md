# BC resource_document (T2 leftover)

HITL ważność dokumentu floty per tenant. document_kind licence|insurance|other
+ valid_until + FK resource. Nie party_document. Nie 409 na trip.

## Dozwolone zależności
- `app.models.resource_document`
- `app.repositories.resource_documents`
- `app.domain`

## Zakaz
- import innych BC services (resources, parties, trips, charges)
- zapis `resource` / `party` / `trip` / `charge` / `party_document`
- countdown / 409 przy planowaniu / HW
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
