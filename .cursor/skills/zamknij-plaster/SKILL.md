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
8. Ustaw `docs/state/CURRENT.md` na **następną pozycję Q** z `docs/PLAN-REALIZACJA.md` § Kolejka (nie pytaj „co chcesz”). Jeśli następne Q to wydmuszka albo wiersz Fali S: **Etap: Plan**, komenda `/plan-modul`, nie `/plaster`. Jeśli następne Q to Fala E `/refaktor` (Q-E1 i sloty): **Etap: Refaktor**, komenda `/refaktor`. Po **Q-E4**: następny = **S1**, nie F9.1. F9.1 bez nazwy — nie ustawiaj jako Następny (żywe nazwy dopiero S56–S58).
8b. `just docs` — przepisuje README / ARCHITECTURE / PLAN z CURRENT. Potem `just docs-check`. GitHub = ten README **po pushu**.
8c. **Bramka przed push** włączona: `git config --get core.hooksPath` = `scripts/githooks`. Brak → `just hooks`. Hook `scripts/githooks/pre-push` odpala `just gate` i zatrzymuje push, gdy bramka pada — tego kroku nie zastępuje ręczne `just gate` z punktu 1.
8d. Zmiana `AGENTS.md` / `GROUNDING.md` / `.cursor/rules/*` bez przepisanego baseline zawsze daje czerwony CI (6 z 7 runów #79-#88). Przy takiej zmianie: `python scripts/quality/agentlint.py --write` + `scripts/quality/agentlint.baseline.json` w tym samym commicie. Sprawdzenie: `just meta-gate` (ok. 1 s).
8e. `python scripts/quality/factory_cycle.py --close` — styl slopu, bench, karta z powtórzonych czerwonych CI, podłoga w górę / sufit funkcji w dół. `just meta-gate` łapie OS-3 (test / how-to / delta) i OS-4 (`craft-style`). Operator nie redaguje. **Nie** dopisuj zasad do AGENTS. **Nie** ruszaj GROUNDING.
8f. `just meta-gate` — jeśli C2 pada na kontrakcie: **osobny** commit higieny cytatu + `agentlint.py --write`. To nie jest Auto-AGENTS. Zero nowych zasad.
9. Commit + push: `feat(M-xx): opis [plaster id]` — **dopiero potem** wolno startować kolejny plaster. `git push --no-verify` tylko z powodem wpisanym do `docs/ops/docs-debt.md`. PRZESZŁO / następny cykl tylko gdy `gh` workflow `gate` na SHA close = `success`; `cancelled` ≠ zielone.
10. **Nowa rozmowa Cursor** — nie kontynuuj w tym wątku.
    **Wyjątek `/noc`:** nie nowa rozmowa — wróć do pętli albo napisz raport (`docs/ops/nocna-zmiana.md`).
