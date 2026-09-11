# BC remediation_option (CI6)

HITL katalog opcji naprawy per tenant. option_code + option_kind + source_ref. Nie kwota. Nie S11.

## Dozwolone zależności
- `app.models.remediation_option`
- `app.repositories.remediation_options`
- `app.domain`

## Zakaz
- import innych BC services (charges, capa_marks, operator_decisions, extraction)
- zapis `charge` / `capa_mark` / `operator_decision` / `mail_draft`
- repair_cost / expected_save / kwota / marża / float
- HTTP / auto-send S11
- UPDATE / DELETE wiersza
