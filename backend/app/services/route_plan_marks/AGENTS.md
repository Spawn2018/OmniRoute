# BC route_plan_mark (BR3.0)

HITL katalog znacznika planu trasy per tenant. mark_code + plan_kind
route|stop|window|other + source_ref. Nie Valhalla. Nie VRP.

## Dozwolone zależności
- `app.models.route_plan_mark`
- `app.repositories.route_plan_marks`
- `app.domain`

## Zakaz
- import innych BC services (load_plan_marks, routing_guides, circle_sims, charges, extraction)
- zapis `load_plan_mark` / `routing_guide` / `circle_sim` / `charge` / `trip`
- Valhalla / ORS / VROOM / LLM-VRP / km / mapa
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
