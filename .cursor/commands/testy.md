---
description: Pisze testy z kryteriów akceptacji, bez implementacji
---

Z `docs/deltas/open/<id>.md` weź kryteria akceptacji.

Dla każdego kryterium napisz test, który MUSI FAILOWAĆ przy obecnym kodzie.

Zasady:
- reguły biznesowe → property-based (hypothesis), nie przykładowe wartości
- nowa tabela → test izolacji tenantów wg wzorca z `tests/patterns/`
- nazwa testu to zdanie opisujące regułę
- Postgres przez testcontainers, nigdy SQLite
- bez mockowania własnego kodu

Uruchom `pytest` i pokaż, że wszystkie nowe testy failują.
NIE PISZ IMPLEMENTACJI.
