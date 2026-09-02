# Tools — mapa bramki

`just gate` lokalnie woła `scripts/quality/run_gate.py`: **zbiera** `code-gate` i `meta-gate`, nie przerywa po pierwszym (E2). CI ma dwa niezależne joby.

## Co naprawdę egzekwuje

| Recipe | Czas rzędu | Egzekucja |
|---|---|---|
| `just meta-gate` | ~1 s | `docs-check`, `agent-refs` (w tym C2), `agentlint`, `craft-check`, `craft-style`, `quality-floor` |
| `just code-gate` | dziesiątki sekund | ruff, mypy, unit, arch, frontend, dup, perf, e2e |
| `just gate` | suma obu | oba wyniki na ekranie, exit ≠ 0 jeśli którykolwiek padł |
| `just agentlint --write` | nie istnieje | `python scripts/quality/agentlint.py --write` |
| `just perf` | w gate | size-limit JS; **k6 = echo** |
| `just dead` | echo | nie DoD |
| `just promptfoo` | CI | fixture, nie żywy OpenAI |

## Taśma komend (nie pomijaj)

| Komenda | Wejście |
|---|---|
| `/plan-modul` | `python scripts/quality/factory_cycle.py --start plan` |
| `/plaster` | `python scripts/quality/factory_cycle.py --start plaster` |
| `/refaktor` | `python scripts/quality/factory_cycle.py --start refactor` |
| `/noc` | `noc-preflight.ps1` → `factory_cycle --start noc` |
| `/zamknij` | `python scripts/quality/factory_cycle.py --close` |

`--close` = bench + karta z powtórzonych czerwonych CI + styl slopu + podłoga w górę / sufit funkcji w dół.
`craft-check` = RLS + OS-3 (test z kodem, how-to albo leftover, delta zanim produkt).
`craft-style` = OS-4 (TODO, except Exception, echo-komentarz, float, as any). Nie „jak człowiek”.
Nie edytuje GROUNDING. Nie dopisuje zasad do AGENTS.

**Źródło:** PLAN § Gate dziś vs cel DoD. Nie zgaduj, który recipe jest stubem.
