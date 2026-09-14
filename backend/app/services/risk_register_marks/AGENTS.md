# BC risk_register_mark (AI9.2)

HITL katalog rejestru ryzyka per tenant. mark_code +
risk_kind open|mitigated|accepted|other + source_ref. Nie scoring osoby. Nie L3 silnik. Nie U-art50 UI.

## Dozwolone zależności
- `app.models.risk_register_mark`
- `app.repositories.risk_register_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, extraction, autonomy_levels, mobile_client_marks)
- zapis `charge` / `extraction_draft` / `autonomy_level`
- scoring osoby · L3 silnik · Mob Expo · U-art50 UI
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
