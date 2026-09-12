# BC e_delivery_mark (EXP2.19)

HITL katalog znacznika e-Doręczeń per tenant. mark_code + delivery_kind
edor|registered|receipt|other + source_ref. Nie PUDO HTTP. Nie live.
Obok `mail_draft` — tu kanał doręczenia, nie szkic maila.

## Dozwolone zależności
- `app.models.e_delivery_mark`
- `app.repositories.e_delivery_marks`
- `app.domain`

## Zakaz
- import innych BC services (mail_drafts, shipments, charges, extraction)
- zapis `mail_draft` / `shipment` / `charge` / `extraction_draft`
- e-Doręczenia live · PUDO HTTP · bajty dowodu
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
