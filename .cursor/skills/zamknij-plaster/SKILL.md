---
name: zamknij-plaster
description: Zamyka plaster, archiwizuje delta-spec, przygotowuje następną rozmowę
---

# Zamknij plaster

1. `/bramka` — weryfikator + audytor (jeśli SQL)
2. Scal delta → `docs/spec/` jeśli wymagane
3. Przenieś `docs/deltas/open/<id>.md` → `docs/deltas/archived/`
4. Linia w `docs/state/PROGRESS.md`
5. Ustaw `docs/state/CURRENT.md` na następny plaster
6. Commit: `feat(M-xx): opis [plaster id]`
7. **Nowa rozmowa Cursor** — nie kontynuuj w tym wątku
