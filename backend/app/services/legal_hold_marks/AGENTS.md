# BC legal_hold_mark (G8)

HITL katalog znacznika retencji/legal hold/eIDAS per tenant. mark_code + hold_kind retention|legal_hold|eidas + source_ref. Nie eIDAS crypto. Nie wipe.

## Dozwolone zależności
- `app.models.legal_hold_mark`
- `app.repositories.legal_hold_marks`
- `app.domain`

## Zakaz
- import innych BC services (gdpr_requests, customer_contracts, charges, extraction)
- zapis `gdpr_request` / `charge` / `customer_contract` / `app_user`
- eIDAS crypto / wipe ciphertext / F1 KSeF / amount / wipe / float / kwota
- HTTP
- UPDATE / DELETE wiersza
