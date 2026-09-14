# BC l3_gate_mark (AI8.2)

HITL katalog checklisty bramy L3 per tenant. mark_code +
gate_kind sot|owner|exception|rollback|blast|other + source_ref. Nie silnik L3 write. Nie mutacja autonomy_level.

## Dozwolone zależności
- `app.models.l3_gate_mark`
- `app.repositories.l3_gate_marks`
- `app.domain`

## Zakaz
- import innych BC services (charges, extraction, autonomy_levels, automation_bias_marks)
- zapis `charge` / `extraction_draft` / `autonomy_level`
- L3 write · scoring Pain×Frequency · Bertha · mutacja autonomy_level
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
