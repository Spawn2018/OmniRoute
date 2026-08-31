# Pętla po każdym kroku planu

Obowiązkowa **przed** push i przed następnym plasterem. Nie zastępuje `just gate`.
`just docs` / `just dead` = `echo` — nie DoD, nie wołaj ich tu. `just perf` = size-limit initial JS (U-size-limit-real).

Bramka (`/bramka`, skill `pr-review`) **mierzy** i nie naprawia.
Ten plik: po tabeli **napraw** to, co nie psuje jakości; reszta → [docs-debt.md](docs-debt.md).

## Tabela (wklej do delty albo jedną linię w PROGRESS)

| Pytanie | Werdykt | Notatka |
|---|---|---|
| Skuteczność | PRZESZŁO / NIE / STUB | kryteria delty vs hello/echo/no-op |
| Szybkość | N/A ten plaster / PRZESZŁO / NIE | tylko ścieżki z budżetu w AGENTS.md; inaczej N/A |
| Dług w diffie | OK / 1–3 poprawki / leftover | `just complexity` + `just dup` na plikach z `git diff` |
| Docs/OS | PRZESZŁO / NIE | CURRENT, PLAN nagłówek, spec z CURRENT, skill jeśli dotyczy |

## Naprawa

- Max 3 zmiany behawioralnie neutralne w tym samym plasterze.
- Zakaz fałszywego `refactor_ratio` i person `.cursor/agents/`.
- Canvas / audyt = przegląd, nie lista do kodu.
- Po naprawie zaktualizuj [docs-debt.md](docs-debt.md) (kolejność + dlaczego).

## Dopiero potem

Skill `zamknij-plaster`: archiwum delty, CURRENT/PROGRESS, commit, **push**. WIP=1.
