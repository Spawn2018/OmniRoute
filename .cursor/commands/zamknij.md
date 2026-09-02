---
description: Zamyka plaster i przygotowuje następny
---

1. Człowiek + `just gate` + skill `zamknij-plaster` (w tym pętla `docs/ops/post-plaster.md`).
2. Sprawdź, czy `docs/deltas/open/` jest puste (albo tylko bieżąca delta).
3. Utwórz commit wg konwencji: `feat(M-xx): <opis> [plaster <id>]`
   ze stopką `Co-authored-by: Cursor Agent <agent@cursor.sh>`.
4. Zaktualizuj `docs/state/CURRENT.md` na **następną pozycję Q** z `docs/PLAN-REALIZACJA.md` (wydmuszka → Etap Plan, `/plan-modul`).
4b. `just docs` (przepisze README na GitHub po pushu).
5. **Bramka przed push:** `git config --get core.hooksPath` musi dać `scripts/githooks`.
   Brak → `just hooks` (albo `scripts/install-hooks.ps1`). Hook odpala `just gate` i blokuje
   czerwony push. `git push --no-verify` to wyjątek do uzasadnienia, nie skrót.
5b. Ruszałeś `AGENTS.md`, `GROUNDING.md` albo `.cursor/rules/*`? Przepisz baseline
   (`python scripts/quality/agentlint.py --write`) i włóż `scripts/quality/agentlint.baseline.json`
   do **tego samego** commita. Bez tego agentlint pada — to była przyczyna 6 z 7 czerwonych
   runów #79-#88. Kontrola trwa sekundę: `just meta-gate`.
5c. `python scripts/quality/factory_cycle.py --close`, potem `just meta-gate`.
    Bench + karta z powtórzonych czerwonych CI + podłoga jakości w górę.
    C2 pada → osobny commit higieny cytatu + agentlint, **nie** nowe zasady,
    **nie** GROUNDING.
6. Wypisz jednym zdaniem, co zostało niedokończone albo odłożone (`docs/ops/docs-debt.md`).

Po tym kroku otwieram nową rozmowę. Nie kontynuuj.

**Wyjątek `/noc`:** nie otwieraj nowej rozmowy. Po pushu wróć do pętli z `docs/ops/nocna-zmiana.md` (albo raport, jeśli minęła godzina stopu).
