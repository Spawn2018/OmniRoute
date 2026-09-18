# BC postal_epo_mark (F11 leftover)

HITL katalog stancji EPO/PP per tenant. mark_code + epo_kind
register|label|track|other + source_ref. Nie live PP. Nie e-Doręczenia.

## Dozwolone zależności
- pp.models.postal_epo_mark
- pp.repositories.postal_epo_marks
- pp.domain

## Zakaz
- import innych BC services (postal_dispatch_marks, e_doreczenia_marks, charges)
- zapis postal_dispatch_mark / e_doreczenia_mark / charge
- live PP / e-Doręczenia HTTP
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
