# customer_contract (CI9)

Katalog nagłówka umowy klienta per tenant. HITL kod + etykiety załadowca/odbiorca. 272.0 = nagłówek. 273.0 = opaque blob present/absent, nie szyfr.

- RLS FORCE. OpenFGA `can_manage_customer_contracts` = member
- `contract_code`: snake 2–32
- `shipper_label` / `their_customer_label`: tekst 1–128 (etykiety, nie FK `party`)
- Unique `(organization_id, contract_code)` i `(organization_id, source_ref)`
- Katalog INSERT, bez UPDATE/DELETE
- 273.0: nullable `blob_ciphertext` BYTEA (fixture HITL). GET zwraca `has_ciphertext`, nigdy bajtów
- ExtractionService nie importuje tego BC
- Job: `/customer-contracts`

Delta: [273.0](../deltas/archived/273.0-customer-contract-ciphertext.md) · [272.0](../deltas/archived/272.0-customer-contract.md).
