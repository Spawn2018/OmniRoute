---
description: Pętla po kroku planu — pomiar, potem naprawa
---

1. `/bramka` najpierw (tylko pomiar, bez naprawy).
2. Skopiuj tabelę **1:1** z `docs/ops/post-plaster.md` — wszystkie wiersze:
   skuteczność, szybkość, SQL, N+1, dług/człowiek, proza operatora, Docs/OS.
   Zero skrótu do czterech starych pytań.
3. Napraw max 3 rzeczy, które nie psują jakości. Reszta → `docs/ops/docs-debt.md`.
4. Dopiero potem skill `zamknij-plaster` (archiwum, CURRENT, `just docs`, commit, push).

`just docs` woła `/zamknij` — to nie echo. `just dead` = echo, nie DoD. `just perf` = size-limit (w gate).
