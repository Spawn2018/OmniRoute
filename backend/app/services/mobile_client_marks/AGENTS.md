# BC mobile_client_mark (Mob)

HITL katalog znacznika klienta mobilnego per tenant. mark_code + client_kind
ios|android|ota|other + source_ref. Nie Expo. Nie EAS. Nie kwota.

## Dozwolone zależności
- `app.models.mobile_client_mark`
- `app.repositories.mobile_client_marks`
- `app.domain`

## Zakaz
- import innych BC services (idp_connectors, charges, extraction)
- zapis `idp_connector` / `charge` / `extraction_draft`
- Expo / EAS OTA live / store submit / kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
