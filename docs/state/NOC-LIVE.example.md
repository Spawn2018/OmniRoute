# Bicie serca nocy (szablon)

Agent `/noc` kopiuje ten kształt do lokalnego pliku o nazwie `NOC-LIVE.md` **w tym samym katalogu**. Żywy plik jest w `.gitignore` i nie wchodzi do gita.

Koordynator (`/noc 7`) ustawia `role: coordinator`. Pomocnik (`noc-preflight.ps1 -Helper`) nie nadpisuje `until` ani `role`.

```
until: 2026-09-10T07:00:00+02:00
status: idle
last_beat: 2026-09-10T03:30:00+02:00
role: coordinator
lease_id: noc-2026-09-10
current_cmd:
claimed: docs/deltas/open/**
helper_worktree:
helper_last_beat:
```

`status`: `busy` (pytest/commit/push na `main`), `idle` (między cyklami), `stop` (zmiana skończona).

`last_beat`: odświeżaj przy starcie cyklu, po pushu, przy `idle`/`stop`. **`busy` + `last_beat` starszy niż 25 min = sesja martwa** (nie „trwa gate”) — strażnik `loop-noc` odzyskuje: ubij orphan `python`/`git`, `idle`, jeden cykl.

`current_cmd`: krótki opis bieżącej komendy (np. `push 486.0 gate`) — opcjonalnie, ułatwia odzysk.

`claimed`: globy, które wolno pisać w worktree. Nigdy `docs/state/CURRENT.md`, `docs/PLAN-REALIZACJA.md`, `backend/alembic/versions/**`.
