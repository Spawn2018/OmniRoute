# tenant_contract_kek (CI9)

Katalog znacznika owijki per tenant. HITL kod + `wrap_kind`. To jest znacznik, nie klucz. 273.0 nadal nie jest szyfrowaniem.

- RLS FORCE. OpenFGA `can_manage_tenant_contract_keks` = member
- `kek_code`: snake 2–32
- `wrap_kind`: `password` | `kms` (token danych, nie live call)
- Unique `(organization_id, kek_code)` i `(organization_id, source_ref)`
- Katalog INSERT, bez UPDATE/DELETE
- Zero BYTEA / ciphertext / hasła / `wrapped_dek`
- GET nigdy nie zwraca materiału klucza
- ExtractionService nie importuje tego BC
- Job: `/tenant-contract-keks`

Delta: [274.0](../deltas/open/274.0-tenant-contract-kek.md).
