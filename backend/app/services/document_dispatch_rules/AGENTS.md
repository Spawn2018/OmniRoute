# BC document_dispatch_rule (I3)

Katalog adresata dokumentów per tenant. Trójka → rola. Nie send. Nie mail_draft.

## Dozwolone zależności
- `app.models.document_dispatch_rule`
- `app.repositories.document_dispatch_rules`
- `app.domain`

## Zakaz
- import innych BC services (quotations, shipments, mail_drafts, charges)
- zapis `shipment` / `mail_draft` / `shipment_document` / `charge`
- kwoty / marża / float / auto-send
- HTTP / Selenium
