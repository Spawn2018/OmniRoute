# BC local_charge_warning_mark (P4c leftover)

HITL katalog stance ostrzeżenia braku dopłaty per tenant. mark_code +
warning_kind warn|hold|waived|other + source_ref.
Nie warning-jako-fakt. Nie matching. Nie 409 wyceny.

## Dozwolone zależności
- `app.models.local_charge_warning_mark`
- `app.repositories.local_charge_warning_marks`
- `app.domain`

## Zakaz
- import innych BC services (local_charges, charges, quotations, extraction)
- zapis `local_charge` / `charge` / `quotation` / `extraction_draft`
- warning-jako-fakt / matching SQL / 409 na wycenie
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `local_charge` / `quotation`
