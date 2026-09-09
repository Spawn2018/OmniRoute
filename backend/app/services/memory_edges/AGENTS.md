# BC memory_edge (W3)

HITL katalog rodzaju krawędzi pamięci per tenant. edge_kind. Nie graf na zdarzeniach. Nie wyszukiwanie stawek.

## Dozwolone zależności
- `app.models.memory_edge`
- `app.repositories.memory_edges`
- `app.domain`

## Zakaz
- import innych BC services (entity_events, charges, extraction, war_room_marks)
- zapis `entity_event` / `charge` / `rate_line` / `extraction_draft`
- graf wektorowy / pgvector / kwota / marża / float
- HTTP / LLM
