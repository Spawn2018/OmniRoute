# BC exchange_connector (S55)

HITL katalog konektora giełdy per tenant. connector_code + system_kind `trans_eu` + source_ref. Nie live HTTP. Nie sekrety. Nie SPA.

## Dozwolone zależności
- `app.models.exchange_connector`
- `app.repositories.exchange_connectors`
- `app.domain`

## Zakaz
- import innych BC services (charges, networks, mail_drafts, outbox_events, idp_connectors, extraction)
- zapis `charge` / `network` / `mail_draft` / `outbox_event` / `idp_connector`
- Trans.eu / TIMOCOM live / scrape / auto-post frachtu / kwota / marża / float
- HTTP / X1–X5 SPA / OAuth2 / pięć tablic
- UPDATE / DELETE wiersza
- kolumny sekretu / ciphertext / `base_url`
