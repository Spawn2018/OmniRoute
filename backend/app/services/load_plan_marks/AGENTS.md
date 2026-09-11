# BC load_plan_mark (G6)

HITL katalog znacznika planu załadunku per tenant. mark_code + stance_kind axes|tunnel|other + source_ref. Nie solver OR. Nie kwota.

## Dozwolone zależności
- `app.models.load_plan_mark`
- `app.repositories.load_plan_marks`
- `app.domain`

## Zakaz
- import innych BC services (dangerous_goods, charges, extraction, trips, resources)
- zapis `dangerous_good` / `charge` / `trip` / `shipment`
- solver OR / LLM-VRP / osie Decimal / amount / axle / float / kwota
- HTTP
- UPDATE / DELETE wiersza
