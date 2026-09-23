# BC network_print_gate_mark (D9c leftover)

HITL katalog stance bramy wydruku sieci per tenant. mark_code +
gate_kind block_409|warn_only|record_only|other + source_ref.
Nie live 409. Nie PDF. Nie matching.

## Dozwolone zależności
- `app.models.network_print_gate_mark`
- `app.repositories.network_print_gate_marks`
- `app.domain`

## Zakaz
- import innych BC services (network_print_requirements, shipments, charges, extraction)
- zapis `network_print_requirement` / `shipment` / `charge` / `extraction_draft`
- live 409 / PDF / QR / ZPL / matching SQL
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `network_print_requirement` / `shipment`
