# BC local_charge_bind_mark (P4c leftover bind)

HITL katalog stance wiązania dopłaty lokalnej per tenant. mark_code +
bind_kind charge|quote|other + source_ref.
Nie FK UUID. Nie matching SQL. Nie warning-jako-fakt.

## Dozwolone zaleznosci
- `app.models.local_charge_bind_mark`
- `app.repositories.local_charge_bind_marks`
- `app.domain`

## Zakaz
- import innych BC services (local_charges, local_charge_warning_marks,
  local_charge_match_marks, charges, quotations, extraction)
- zapis `local_charge` / `charge` / `quotation` / `extraction_draft`
- FK UUID / matching SQL / warning-jako-fakt / druga marza
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `local_charge` / `quotation` / `charge`
