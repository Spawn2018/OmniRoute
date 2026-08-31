---
description: Zamyka plaster i przygotowuje następny
---

1. Człowiek + `just gate` + skill `zamknij-plaster` (w tym pętla `docs/ops/post-plaster.md`).
2. Sprawdź, czy `docs/deltas/open/` jest puste (albo tylko bieżąca delta).
3. Utwórz commit wg konwencji: `feat(M-xx): <opis> [plaster <id>]`
   ze stopką `Co-authored-by: Cursor Agent <agent@cursor.sh>`.
4. Zaktualizuj `docs/state/CURRENT.md` na następny plaster z planu.
5. Wypisz jednym zdaniem, co zostało niedokończone albo odłożone (`docs/ops/docs-debt.md`).

Po tym kroku otwieram nową rozmowę. Nie kontynuuj.
