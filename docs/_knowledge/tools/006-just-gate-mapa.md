# Tools — mapa bramki

`just gate` lokalnie = `code-gate` potem `meta-gate`. Just **przerywa na pierwszym błędzie** — jeśli padnie ruff, meta się nie wykona. CI woła `gate` i `meta` jako **dwa niezależne joby**.

## Co naprawdę egzekwuje

| Recipe | Czas rzędu | Egzekucja |
|---|---|---|
| `just meta-gate` | ~1 s | `docs-check`, `agent-refs`, `agentlint` |
| `just code-gate` | dziesiątki sekund | ruff, mypy, unit, arch, frontend, dup, perf, e2e |
| `just gate` | ~70 s | oba, fail-fast |
| `just agentlint --write` | nie istnieje | `python scripts/quality/agentlint.py --write` |
| `just perf` | w gate | size-limit JS; **k6 = echo** |
| `just dead` | echo | nie DoD |
| `just promptfoo` | CI | fixture, nie żywy OpenAI |

## Kiedy które

- Zmiana `AGENTS.md` / alwaysApply rules: `python scripts/quality/agentlint.py --write`, baseline w **tym samym** commicie, potem `just meta-gate`.
- Przed pushem: hook `pre-push` = pełne `just gate` (wymaga `just hooks`).
- Czerwony push „od razu”: najpierw `just meta-gate` — seria #79–#88 to był podpis, nie kod.

**Źródło:** PLAN § Gate dziś vs cel DoD. Nie zgaduj, który recipe jest stubem.
