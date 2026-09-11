# Spec: shipment vs routing_guide 409 (CT4 leftover)

**Moduł żywy:** CT4 leftover egzekucja na zleceniu

## 287.0 żywy 409 na shipment

- Gdy istnieje `routing_guide_enforcement.enforcement_kind = block_409`:
  POST `/shipments` wymaga `guide_code` z katalogu `routing_guide` tenanta
- Brak / nieznany → HTTP 409
- `record_only` nie blokuje
- Ta sama bramka domenowa co ASN (286.0)
