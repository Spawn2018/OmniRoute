# B.7 — ochrona `main` (procedura ręczna)

**Status:** obowiązuje od 2026-08-31  
**Powód:** GitHub **Free + private** → branch protection API **HTTP 403**.  
Automatyczne „Require status checks: `gate`” włącza się po **Pro / Team** albo po upublicznieniu repo.

## Procedura (zastępuje branch protection do czasu Pro)

1. **Nie force-push** na `main` (`git push --force` / `--force-with-lease` na main = zabronione).
2. Każda zmiana na `main`: najpierw lokalnie `just gate` (lub CI na push) — **merge/push tylko przy green**.
3. Preferuj PR nawet przy pracy solo; review (ludzki lub Bugbot) przed merge gdy Pro pozwoli na required checks.
4. Po upgrade do Pro/Team: w Settings → Branches → Add rule na `main`:
   - Require a pull request before merging
   - Require status checks to pass: **`gate`**
   - Restrict force pushes
   - Do not allow bypassing the above settings
5. Gdy rule API działa — ten dokument oznacz jako *superseded*; zostaw link w PLAN.

## Egzekucja dziś

- CI `gate` na każdy push do `main` (Actions) — **działa**.
- Brak blokady merge w UI GitHub — **dyscyplina procesu** powyżej.
