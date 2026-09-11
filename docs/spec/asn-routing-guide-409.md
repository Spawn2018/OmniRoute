# Spec: ASN vs routing_guide 409 (CT4 leftover)

**Moduł żywy:** CT4 leftover egzekucja

## 286.0 żywy 409 na ASN

- Gdy istnieje `routing_guide_enforcement.enforcement_kind = block_409`:
  POST `/asns` wymaga `guide_code` z katalogu `routing_guide` tenanta
- Brak / nieznany → HTTP 409
- `record_only` nie blokuje
- Nie 409 na shipment w tym plasterze
