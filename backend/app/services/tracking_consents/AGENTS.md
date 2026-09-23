# BC tracking_consent (BR2.2)

HITL katalog zgody na sledzenie per tenant. consent_code + consent_kind
party|driver|other + source_ref. Bool `party_contact.tracking_consent` jest
w BC parties (634.0) — tu nie mutujesz kontaktu. Nie live poll.

## Dozwolone zaleznosci
- `app.models.tracking_consent`
- `app.repositories.tracking_consents`
- `app.domain`

## Zakaz
- import innych BC services (parties, tracking_events, position_events, charges, extraction)
- zapis `party` / `party_contact` / `tracking_event` / `position_event` / `charge`
- live GPS / poll / mapa / egzekucja zgody
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `party` / `party_contact` / `resource`
