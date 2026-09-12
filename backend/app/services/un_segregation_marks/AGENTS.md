# BC un_segregation_mark (EXP0.9)

HITL katalog znacznika tunel/segregacja UN per tenant. mark_code + segregate_kind
tunnel|segregation|compat|other + source_ref. Nie solver OR. Nie LLM-VRP.

## Dozwolone zależności
- `app.models.un_segregation_mark`
- `app.repositories.un_segregation_marks`
- `app.domain`

## Zakaz
- import innych BC services (load_plan_marks, oog_marks, dangerous_goods, charges, extraction)
- zapis `load_plan_mark` / `oog_mark` / `dangerous_good` / `charge` / `trip`
- solver OR / LLM-VRP / osie Decimal / amount / float / kwota
- HTTP
- UPDATE / DELETE wiersza
