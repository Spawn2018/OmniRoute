---
name: zamknij-plaster
description: Zamyka plaster, archiwizuje delta-spec, przygotowuje następną rozmowę
---

# Zamknij plaster

1. `/bramka` — człowiek + `just gate`
2. **Pętla** `docs/ops/post-plaster.md`: skuteczność, szybkość (lub N/A), dług w diffie, docs/OS. Bramka mierzy; tu naprawiasz to, co nie psuje jakości.
3. Leftovery z „dlaczego” → `docs/ops/docs-debt.md` + PLAN § leftoverów
4. Sprawdź `docs/PLAN-REALIZACJA.md` § Gate dziś — **nie** oznaczaj DoD dla recipe `echo`
5. Scal delta → `docs/spec/` jeśli wymagane
6. Przenieś `docs/deltas/open/<id>.md` → `docs/deltas/archived/`
7. Linia w `docs/state/PROGRESS.md`
8. Ustaw `docs/state/CURRENT.md` na **następną pozycję Q** z `docs/PLAN-REALIZACJA.md` § Kolejka (nie pytaj „co chcesz”). Jeśli następne Q to wydmuszka: **Etap: Plan**, komenda `/plan-modul`, nie `/plaster`.
8b. `just docs` — przepisuje README / ARCHITECTURE / PLAN z CURRENT. Potem `just docs-check`. GitHub = ten README **po pushu**.
9. Commit + push: `feat(M-xx): opis [plaster id]` — **dopiero potem** wolno startować kolejny plaster
10. **Nowa rozmowa Cursor** — nie kontynuuj w tym wątku
