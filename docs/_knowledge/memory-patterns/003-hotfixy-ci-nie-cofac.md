# Memory — hotfixy CI, nie cofać

Pięć napraw z PLAN § Gate. Cofnięcie = powrót do fałszywego zielonego albo do serii czerwonych pushy.

| Co | Dlaczego zostaje |
|---|---|
| `005` `current_database()` zamiast `Connection.url` | URL z konfiguracji kłamał względem sesji |
| agent-refs: URI ≠ plik | link liczy się wobec katalogu pliku, nie ROOT |
| agentlint baseline | podpis kontraktu; hash w innym commicie = czerwień #79–#88 |
| conftest: osobne `DO $$` | jeden blok psuł izolację setupu |
| live HTTP = `httpx` AsyncClient | nie udawaj sieci mockiem tam, gdzie test ma iść na żywą PG |
| `rate_line` mutate = commit + select kolumny | mutacja w teście musi trafić w prawdziwe kolumny |

Nie „upraszczaj” tego przy refaktorze gate. Nowa usterka CI = nowy hotfix i nowa linia tutaj, nie edycja historii.
