---
description: Pętla po kroku planu — pomiar, potem naprawa
---

1. `/bramka` najpierw (tylko pomiar, bez naprawy).
2. Skopiuj tabelę **1:1** z `docs/ops/post-plaster.md` — wszystkie wiersze,
   w tym bench rzemiosła. Zero skrótu.
3. Napraw max 3 rzeczy, które nie psują jakości. Reszta → `docs/ops/docs-debt.md`.
4. `python scripts/quality/factory_cycle.py --close`, potem skill `zamknij-plaster`.

`just docs` woła `/zamknij` — to nie echo. `just dead` = echo, nie DoD. `just perf` = size-limit (w gate).
