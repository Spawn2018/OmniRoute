# Krawędź pamięci

Na `/memory-edges` zapisujesz **znacznik rodzaju krawędzi** tenanta (`recalls`, `follows`, `blocks`, `cites`, `other`). To nie graf na zdarzeniach podmiotu i nie wyszukiwanie stawek.

1. Wejdź na Krawędź pamięci. Wybierz rodzaj (`recalls` / `follows` / `blocks` / `cites` / `other`).
2. Podaj `source_ref` (`fixture://memory-edge/…` albo `tenant:manual`).
3. „Zapisz krawędź pamięci”.

Czego tu nie ma: RAG, pgvector, krawędzie FK na `entity_event`, suma w przeglądarce. Ledger zdarzeń zostaje na `/entity-events`. Marża zostaje na `/charges`.

Nazwy w kodzie: `memory_edge` · `edge_kind` · `source_ref`.
