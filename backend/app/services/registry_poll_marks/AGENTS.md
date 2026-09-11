# BC registry_poll_mark (EXP7.2)

HITL katalog znacznika poll rejestru SaaS Omni per tenant. mark_code + poll_kind
ceidg|krs|vies|whitelist|other + source_ref. Nie live scrape. Nie notice auto.

## Dozwolone zależności
- `app.models.registry_poll_mark`
- `app.repositories.registry_poll_marks`
- `app.domain`

## Zakaz
- import innych BC services (partys, charges, extraction)
- zapis `party` / `charge` / `session` / `extraction_draft`
- live scrape / KRS HTTP / usage SQL / HTTP CEIDG / scrape
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
