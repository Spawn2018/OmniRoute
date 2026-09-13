# BC twin_mark (W1)

HITL katalog rodzaju bliźniaka per tenant. twin_kind. Nie fizyka. Nie plan_snapshot.

## Dozwolone zależności
- `app.models.twin_mark`
- `app.repositories.twin_marks`
- `app.domain`

## Zakaz
- import innych BC services (resources, trips, charges, extraction)
- zapis `resource` / `trip` / `charge` / `container`
- fizyka / circle_sim / kwota / marża / float
- HTTP / plan_snapshot
- import `twin_kinds` (FK rodzaju jest w bazie)
