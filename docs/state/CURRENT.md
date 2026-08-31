# Bieżący focus

**Faza:** Charge  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **1.1** `rate_line` M-07 (zarchiwizowany)  
**Następny:** **Charge 1.2** `charge` buy+sell, marża w kodzie. Równolegle: Auth0 I1, Wave FE U-* (pliki ∩ = ∅). 0.24 pip-audit pominięty (opcjonalny).

**Spec (jedna na sesję):** [docs/state/PROGRAM-12M.md](docs/state/PROGRAM-12M.md) Charge 1.2

**Kanon:** [docs/state/PROGRAM-12M.md](docs/state/PROGRAM-12M.md)

**Uczciwość:** 1.1 = niemutowalna stawka kupna + `source_ref` + `/rate-lines`. Nie tabela `charge`. U-routes-breadth = jedna trasa operatora, **nie** Exit Wave FE. Isolation RLS = CI (lokalnie PG wisiał). Leftover ≠ DONE. echo ≠ DoD.

**Plan:** [docs/PLAN-REALIZACJA.md](docs/PLAN-REALIZACJA.md)

**2026-09-01:** 1.1 — `rate_line` immutable + `source_ref` M-07.
