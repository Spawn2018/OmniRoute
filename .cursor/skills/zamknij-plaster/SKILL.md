---
name: zamknij-plaster
description: Zamyka plaster, archiwizuje delta-spec, przygotowuje następną rozmowę
---

# Zamknij plaster

1. `/bramka` — weryfikator + audytor (jeśli SQL)
2. Sprawdź `docs/PLAN-REALIZACJA.md` § Gate dziś — **nie** oznaczaj DoD dla recipe `echo`
3. Scal delta → `docs/spec/` jeśli wymagane
4. Przenieś `docs/deltas/open/<id>.md` → `docs/deltas/archived/`
5. Linia w `docs/state/PROGRESS.md`
6. Ustaw `docs/state/CURRENT.md` na następny plaster
7. Commit + push: `feat(M-xx): opis [plaster id]` — **dopiero potem** wolno startować kolejny plaster
8. **Nowa rozmowa Cursor** — nie kontynuuj w tym wątku
