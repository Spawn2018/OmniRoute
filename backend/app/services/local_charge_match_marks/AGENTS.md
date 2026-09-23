# BC local_charge_match_mark (P4c leftover matching)

HITL katalog stance dopasowania dopłaty lokalnej per tenant. mark_code +
match_kind match|gap|waive|other + source_ref.
Nie matching SQL vs local_charge. Nie druga marza.

## Dozwolone zaleznosci
- `app.models.local_charge_match_mark`
- `app.repositories.local_charge_match_marks`
- `app.domain`

## Zakaz
- import innych BC services (local_charges, local_charge_warning_marks, charges, extraction)
- zapis `local_charge` / `local_charge_warning_mark` / `charge` / `extraction_draft`
- matching SQL vs local_charge / warning-jako-fakt / druga marza
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `local_charge` / `quotation` / `charge`
