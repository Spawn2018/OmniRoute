# Machine — jeden pisarz na drzewie

**Status:** machine. Zdarzenie 2026-09-02: commit fabryki wszedł pod plaster 66.0,
bo dwóch pisarzy było na tym samym `main`.

## Sygnał

`git status --porcelain` pokazuje pliki poza indeksem w chwili `git commit`.
Albo `docs/state/NOC-LIVE.md` ≠ `stop` przy starcie `/plaster`.

## Zamiast

- `scripts/githooks/pre-commit` → `scripts/quality/pre_commit_factory.py`
- `/plaster` i `/plan-modul`: `python scripts/quality/writer_preflight.py`
- Fabryka poza Q: worktree + osobna gałąź; merge po czystym drzewie
- Nie rebase / nie force-push commita produktu (`0224f1b`)

## Zakaz

- Drugi `/plaster` albo `/noc` na tym samym checkout
- `--no-verify`, żeby „przeskoczyć drugiego pisarza”
- Auto-merge
