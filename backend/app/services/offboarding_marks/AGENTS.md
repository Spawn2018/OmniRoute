# BC offboarding_mark (EXP2.28)

HITL katalog znacznika offboarding per tenant. mark_code + offboard_kind
offboard|export|revoke|other + source_ref. Nie wipe ciphertext. Nie DELETE konta.

## Dozwolone zaleznosci
- `app.models.offboarding_mark`
- `app.repositories.offboarding_marks`
- `app.domain`

## Zakaz
- import innych BC services (gdpr_requests, legal_hold_marks, charges, extraction)
- zapis `gdpr_request` / `legal_hold_mark` / `app_user` / `charge`
- wipe ciphertext · DELETE konta · eIDAS crypto
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
