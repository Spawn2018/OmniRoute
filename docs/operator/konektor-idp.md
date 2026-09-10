# Konektor Auth0

Na `/idp-connectors` dopisujesz **konektor IdP** tenanta: kod snake oraz token `auth0`. To nie jest logowanie. JWT hello i hasło zostają na `/session`.

1. Wejdź na Konektor Auth0. Wpisz kod (`auth0_eu_desk` — snake 2–32).
2. Dostawcę zostaw `auth0`. Inny IdP (Okta, Azure) nie wejdzie — to osobne leftovery.
3. Opcjonalnie wpisz domenę publiczną jako host (`acme.eu.auth0.com`), bez `https://`. To tekst, nie issuer do JWKS.
4. Podaj `source_ref` (`fixture://auth0/…` albo `tenant:manual`).
5. „Zapisz konektor Auth0”. Ten sam kod albo to samo `source_ref` u tenanta nie wejdzie drugi raz.

Czego tu nie ma: przycisk logowania, redirect OAuth, BFF, PKCE, JWKS, `client_secret`, ciphertext, Organizations, Infisical, portale. Marża zostaje na `/charges`. Sesja zostaje na `/session`.

Nazwy w kodzie: `idp_connector` · `connector_code` · `provider_code` · `public_domain` · `source_ref`.
