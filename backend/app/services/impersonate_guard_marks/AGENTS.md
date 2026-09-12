# BC impersonate_guard_mark (EXP0.12)

HITL katalog znacznika reguły Admin-P per tenant. mark_code + guard_kind
impersonate|unwrap_denied|other + source_ref. Nie unwrap. Nie Auth0 live.

## Dozwolone zależności
- `app.models.impersonate_guard_mark`
- `app.repositories.impersonate_guard_marks`
- `app.domain`

## Zakaz
- import innych BC services (customer_contracts, tenant_contract_keks, charges, extraction)
- zapis `customer_contract` / `tenant_contract_kek` / `charge` / `extraction_draft`
- unwrap KEK / Fernet / KMS / Auth0 impersonate live / ciphertext
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- kolumny sekretu / ciphertext / wrapped_dek
