# BC tenant_contract_kek (CI9)

HITL katalog znacznika owijki per tenant. kek_code + wrap_kind `password`|`kms` + source_ref. Nie klucz. Nie materiał. Nie KMS.

## Dozwolone zależności
- `app.models.tenant_contract_kek`
- `app.repositories.tenant_contract_keks`
- `app.domain`

## Zakaz
- import innych BC services (customer_contracts, charges, extraction)
- zapis `customer_contract` / `charge` / `extraction_draft`
- BYTEA / wrapped_dek / ciphertext / hasło / materiał klucza
- KMS HTTP / unwrap / Fernet / AES / Omni-master / kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- kolumny sekretu
