# BC idp_connector (S53)

HITL katalog konektora IdP per tenant. connector_code + provider_code `auth0` + source_ref. Nie login. Nie live HTTP. Nie sekrety.

## Dozwolone zależności
- `app.models.idp_connector`
- `app.repositories.idp_connectors`
- `app.domain`

## Zakaz
- import innych BC services (tenancy, charges, extraction, session)
- zapis `app_user` / `charge` / `session` / `refresh_token`
- Auth0 SDK / JWKS / PKCE / BFF / cookie / kwota / marża / float
- HTTP / Organizations / Infisical / pięć IdP
- UPDATE / DELETE wiersza
- kolumny sekretu / ciphertext / `client_secret`
