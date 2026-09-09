# BC war_room_mark (W2)

HITL katalog rodzaju incydentu sali per tenant. incident_kind. Nie scalanie alertów. Nie drugi czat.

## Dozwolone zależności
- `app.models.war_room_mark`
- `app.repositories.war_room_marks`
- `app.domain`

## Zakaz
- import innych BC services (exceptions, tower_impacts, charges, extraction)
- zapis `operational_exception` / `tower_impact` / `charge` / `operator_decision`
- scalanie alertów / drugi czat / kwota / marża / float
- HTTP / T8 live API / mapa
