# BC gdpr_request (M-56)

Wniosek RODO per tenant. Wiąże `app_user` z rodzajem access/erasure.
Nie DPIA, nie kasowanie wiersza konta, nie live HTTP.

## Dozwolone zależności
- `app.models.gdpr_request`
- `app.repositories.gdpr_requests`
- `app.domain`

## Zakaz
- import innych BC services (tenancy, inbound, parties)
- zapis `app_user` / `inbound_message` / `charge`
- kwoty / marża / float / DELETE konta
- HTTP
