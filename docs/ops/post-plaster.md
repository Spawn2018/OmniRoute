# Pętla po każdym kroku planu

Obowiązkowa **przed** push i przed następnym plasterem. Nie zastępuje `just gate`.
`just docs` = sync statusu z CURRENT.md (README, ARCHITECTURE, PLAN) — realne, woła `/zamknij`. `just dead` = `echo` — nie DoD. `just perf` = size-limit initial JS (U-size-limit-real).

Bramka (`/bramka`, skill `pr-review`) **mierzy** i nie naprawia.
Ten plik: po tabeli **napraw** to, co nie psuje jakości; reszta → [docs-debt.md](docs-debt.md).

To nie jest drugi plan produktu. Gwiazda: [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Cel jakości (4,4–5). `/refaktor` = spłata starego 3,x (max 3); nie zastępuje tej tabeli. Tabela jest na **diffie plastra**. Nota 4,4 stawia karta, nie autorecenzja. Tablice-odczyty nie idą na 5,0.

Po kodzie: komenda `/po-plastrze` (pełna tabela, zero skrótu), dopiero potem `/zamknij`. `/noc` nie pomija tej kartki.

## Tabela (wklej do delty albo jedną linię w PROGRESS)

Skopiuj **wszystkie** wiersze. Nie skracaj do skuteczność / szybkość / dług / docs.

| Pytanie | Werdykt | Notatka |
|---|---|---|
| Skuteczność | PRZESZŁO / NIE / STUB | kryteria delty vs hello/echo/no-op |
| Szybkość | N/A ten plaster / PRZESZŁO / NIE | tylko ścieżki z budżetu w AGENTS.md; inaczej N/A |
| SQL | N/A / EXPLAIN / leftover | nowy albo zmieniony SELECT/INSERT/UPDATE/resolve: `EXPLAIN ANALYZE` albo leftover z powodem. Brak zapytania w diffie = N/A |
| N+1 | OK / 1–3 poprawki / leftover | zakaz pętli z zapytaniem w diffie. Jest `for` + `session` / `execute` / `fetch` — wyciąć albo leftover |
| Dług / człowiek | OK / 1–3 poprawki / leftover | `just complexity` + `just dup` na plikach z `git diff`. Komentarz tylko *dlaczego*. Trzecie powtórzenie wycięte albo leftover. Brak nowej warstwy z jedną implementacją |
| Proza operatora | N/A / 5–15 zdań / leftover | tylko gdy plaster dał **job zapisu** (nie panel-odczyt cudzej tabeli). Brak `docs/operator/` = leftover z „dlaczego nie”, nie 70 stubów |
| Docs/OS | PRZESZŁO / NIE | CURRENT, potem `just docs`; spec z CURRENT; skill jeśli dotyczy |
| Pushy do zielonego | liczba / N/A | agent z `gh run list` albo N/A; **nie** job operatora |
| Minuty plastra | liczba / N/A | zegar sesji agenta albo N/A; zakaz optymalizacji pod tę liczbę |
| Bench rzemiosła | PRZESZŁO / NIE | `factory_cycle.py --close`; OS-3 w `craft-check` (test, how-to, delta) |

**Nie w tej tabeli** (osobne Q albo `/refaktor`): CodeQL, mutacje, STRIDE, C4, changelog od zera, mixin wszystkich modeli, vulture, k6 jako DoD, Alembic vs `create_all`.

## Naprawa

- Max 3 zmiany behawioralnie neutralne w tym samym plasterze.
- Zakaz fałszywego `refactor_ratio` i person `.cursor/agents/`.
- Canvas / audyt = przegląd, nie lista do kodu.
- Po naprawie zaktualizuj [docs-debt.md](docs-debt.md) (kolejność + dlaczego).

## Dopiero potem

Skill `zamknij-plaster`: archiwum delty, CURRENT/PROGRESS, commit, **push**. WIP=1.

Push przechodzi przez hook `scripts/githooks/pre-push` (włącz raz: `just hooks`), który
odpala `just gate` i przerywa push przy błędzie. Nie zwalnia to z tabeli powyżej — hook
sprawdza bramkę, nie skuteczność ani dług w diffie.

`gate` = `code-gate` (ruff, mypy, testy, import-linter, frontend, dup, perf) i dopiero potem
`meta-gate` (docs-check, agent-refs, agentlint). Kolejność jest z audytu runów #79-#88:
meta stojące pierwsze przerywało bramkę i przez siedem pushy CI nie powiedziało nic o kodzie.
W CI oba idą jako niezależne joby, więc czerwona dokumentacja nie przykrywa wyniku kodu.
