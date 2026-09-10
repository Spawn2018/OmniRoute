# BC customer_contract (CI9)

HITL katalog nagłówka umowy per tenant. contract_code + etykiety shipper/their_customer + source_ref. Nie treść. Nie ciphertext. Nie KEK.

## Dozwolone zależności
- `app.models.customer_contract`
- `app.repositories.customer_contracts`
- `app.domain`

## Zakaz
- import innych BC services (charges, parties, extraction, tenders)
- zapis `charge` / `party` / `extraction_draft` / `sla_clause`
- treść umowy / blob_ciphertext / wrapped_dek / tenant_contract_kek
- KMS / unwrap / klucz Omni-master / super-admin plaintext
- Langfuse na PDF / extract LLM / kwota / marża / float
- HTTP / p44 / FourKites / Shippeo
- UPDATE / DELETE wiersza
