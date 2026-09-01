---
description: Nocna zmiana — jeden zaakceptowany plaster, Cloud Agent
---

Czytaj `docs/state/CURRENT.md` i `docs/ops/nocna-zmiana.md`. Potem wykonaj **tylko** to, co CURRENT pozwala.

Teraz (2026-09-01): Etap = delta **4.1** zaakceptowana. Spec: `docs/spec/geography.md`. Delta: `docs/deltas/open/4.1-location-zones.md`.

1. Tryb Agent. Komenda `/plaster` (plan plików, stop po kroku 6 — tu nie czekasz na człowieka; operator przyjął ryzyko nocnego kodu).
2. `/testy` — czerwone testy z kryteriów delty. Potem implementacja.
3. `just gate`. Czerwone = napraw max dwa razy, potem stop.
4. `/zamknij`: post-plaster, PROGRESS, CURRENT = **Plan 4.2** (nie kod 4.2), commit.
5. Cloud: gałąź + PR, nie force-push na main. CI czerwone = napraw na tej samej gałęzi, max 10 autofix jak w Cloud.
6. Stop. Nie 4.2, nie Q2, nie M-02, nie Auth0.

Kanon: `docs/PLAN-REALIZACJA.md` + GROUNDING.md + GLOSSARY.md.
WIP=1. Decimal. HITL bez zmian. ExtractionService nie importuje rates.
Nie cofaj hotfixów CI: `005` `current_database()`, agent-refs URI, agentlint baseline,
conftest (osobne `DO $$`), live HTTP = `httpx.AsyncClient`, `rate_line` mutate = commit + select kolumny.

W Planie (nie ten bieg): bierz opcję **rekomendowaną**. Brak etykiety → węższa opcja z kolejki Q.
