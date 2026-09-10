# Bicie serca nocy (szablon)

Agent `/noc` kopiuje ten kształt do lokalnego pliku o nazwie `NOC-LIVE.md` **w tym samym katalogu**. Żywy plik jest w `.gitignore` i nie wchodzi do gita.

Koordynator (`/noc 7`) ustawia `role: coordinator`. Pomocnik (`noc-preflight.ps1 -Helper`) nie nadpisuje `until` ani `role`.

```
until: 2026-09-10T07:00:00+02:00
status: idle
last_beat: 2026-09-10T03:30:00+02:00
role: coordinator
lease_id: noc-2026-09-10
claimed: docs/deltas/open/**
helper_worktree:
helper_last_beat:
```

`status`: `busy` (pytest/commit na `main`), `idle` (między cyklami), `stop` (zmiana skończona).

`claimed`: globy, które wolno pisać w worktree. Nigdy `docs/state/CURRENT.md`, `docs/PLAN-REALIZACJA.md`, `backend/alembic/versions/**`.
