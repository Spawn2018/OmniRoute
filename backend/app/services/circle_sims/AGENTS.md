# BC circle_sim (G2.20)

HITL katalog kółka per tenant. sim_code + para UN/LOCODE unload/load + source_ref. Nie silnik ≥500k. Nie km.

## Dozwolone zależności
- `app.models.circle_sim`
- `app.repositories.circle_sims`
- `app.domain`

## Zakaz
- import innych BC services (trips, shipments, resources, charges, geography, tenders)
- zapis `trip` / `shipment` / `charge` / `lane_pattern` / `tender`
- km / VRP / n_overlap / kwota / marża / float
- HTTP / LLM / silnik 500k / what-if
- UPDATE / DELETE wiersza
