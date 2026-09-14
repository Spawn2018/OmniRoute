# BC style_fidelity_mark (AI8.1)

HITL katalog stancji bramki fidelity per tenant. mark_code +
fidelity_kind pass|hold|reject|exempt|other + source_ref.
Nie score 85%. Nie scoring osoby.

## Dozwolone zależności
- `app.models.style_fidelity_mark`
- `app.repositories.style_fidelity_marks`
- `app.domain`

## Zakaz
- import innych BC services (style_cascade_marks, mail_drafts, charges, extraction)
- zapis `style_cascade_mark` / `mail_draft` / `charge` / `party`
- wyliczanie SCORE 85% · LLM porównanie stylu · scoring osoby
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
