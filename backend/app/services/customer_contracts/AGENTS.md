# BC customer_contract (CI9)

HITL katalog nagłówka umowy per tenant. contract_code + etykiety shipper/their_customer + source_ref + opcjonalny opaque BYTEA. Nie treść. Nie szyfr. Nie KEK.

## Dozwolone zależności
- `app.models.customer_contract`
- `app.repositories.customer_contracts`
- `app.domain`

## Zakaz
- import innych BC services (charges, parties, extraction, tenders)
- zapis `charge` / `party` / `extraction_draft` / `sla_clause`
- unwrap / wrapped_dek / tenant_contract_kek / KMS / Fernet / AES
- zwrot blob_ciphertext / plaintext / hex do API
- klucz Omni-master / super-admin decode
- Langfuse na PDF / extract LLM / kwota / marża / float
- HTTP / p44 / FourKites / Shippeo
- UPDATE / DELETE wiersza
