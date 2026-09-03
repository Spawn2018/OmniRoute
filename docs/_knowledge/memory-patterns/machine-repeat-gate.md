# Machine — powtórzony fail CI `gate`

**Status:** machine. Orakulum: `gh run list` co najmniej 3 czerwonych na `main`.
Nie edytuje AGENTS.md ani GROUNDING.md.

## Sygnał

Job/workflow `gate` padł 4 razy w ostatnich 40 runach.

## Zamiast

1. Czytaj komentarz `report-failure` na commicie (code-gate vs meta).
2. Napraw kod albo cytat kontraktu. C2 = higiena, nie nowe zasady.
3. `just meta-gate` przed pushem. `python scripts/quality/agentlint.py --write`
   tylko gdy ruszasz AGENTS/GROUNDING/rules, w **tym samym** commicie.

## Zakaz

- `--no-verify`
- Auto-AGENTS (dopisywanie zasad, żeby gate przeszedł)
- Żywy OpenAI w gate
