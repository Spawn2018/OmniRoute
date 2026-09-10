# customer_contract (CI9)

Katalog nagłówka umowy klienta per tenant. HITL kod + etykiety załadowca/odbiorca. Nie treść. Nie ciphertext. Nie KEK.

- RLS FORCE. OpenFGA `can_manage_customer_contracts` = member
- `contract_code`: snake 2–32
- `shipper_label` / `their_customer_label`: tekst 1–128 (etykiety, nie FK `party`)
- Unique `(organization_id, contract_code)` i `(organization_id, source_ref)`
- Katalog INSERT, bez UPDATE/DELETE
- GET nie zwraca treści umowy — kolumny treści nie ma
- ExtractionService nie importuje tego BC
- Job: `/customer-contracts`

Delta: [272.0](../deltas/archived/272.0-customer-contract.md).
