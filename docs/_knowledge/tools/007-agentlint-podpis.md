# Tools — podpis agentlint

`scripts/quality/agentlint.py` haszuje `AGENTS.md`, `GROUNDING.md` i trzy alwaysApply rules. Zmiana treści bez baseline w **tym samym commicie** = czerwony job `meta` (seria #79–#88).

## Jak

1. Edytuj kontrakt **bez** kodu produktu w tym commicie.
2. `python scripts/quality/agentlint.py --write`
3. `git add` treść **i** `scripts/quality/agentlint.baseline.json`
4. `just meta-gate`
5. Commit. Git hook `pre-commit` odmawia, gdy kontrakt jest w indeksie, a baseline nie.

## Zakaz

- `--write` w `afterFileEdit` (bot podpisuje kontrakt = brak podpisu).
- Hash w commicie B, treść w commicie A.
- Wyłączenie agentlinta na `main`.
- `--no-verify`, żeby „przeskoczyć podpis”.

Lokalny pre-commit odmawia też, gdy w drzewie zostają **inne** brudne pliki niż ten commit — drugi pisarz na tym samym checkout.
