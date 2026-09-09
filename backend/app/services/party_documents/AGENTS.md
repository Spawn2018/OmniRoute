# BC party_document (C8)

HITL rodzaj dokumentu kontrahenta per tenant. document_kind + source_ref na party. Nie 409. Nie extract. Nie marża.

## Dozwolone zależności
- `app.models.party_document`
- `app.repositories.party_documents`
- `app.domain`

## Zakaz
- import innych BC services (parties, shipments, charges, extraction)
- zapis `party` / `shipment` / `charge` / `kreptd_licence`
- 409 na POST shipment / `relation_document_requirement` / HTTP / LLM / kwota / marża / float
- scoring osoby / kolumny na `party` / bajty pliku
