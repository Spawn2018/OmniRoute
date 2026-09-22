# BC network_print_requirement (D9c)

HITL katalog wymogu wydruku sieci per tenant. requirement_code +
network_label + source_ref. Nie 409. Nie PDF. Nie QR.

## Dozwolone zależności
- `app.models.network_print_requirement`
- `app.repositories.network_print_requirements`
- `app.domain`

## Zakaz
- import innych BC services (document_templates, networks, charges, extraction)
- zapis `document_template` / `network` / `charge` / `extraction_draft`
- HTTP 409 na wyjeździe / zleceniu
- PDF / QR / ZPL / bajty
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
