# Bieżący focus

**Faza:** Charge  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **1.2** `charge` M-08 (zarchiwizowany)  
**Następny:** **Charge 1.3** accept → RatesService, ta sama transakcja HTTP. Równolegle: Auth0 I1, Wave FE U-* (pliki ∩ = ∅). 0.24 pip-audit pominięty (opcjonalny).

**Spec (jedna na sesję):** [docs/state/PROGRAM-12M.md](docs/state/PROGRAM-12M.md) Charge 1.3

**Kanon:** [docs/state/PROGRAM-12M.md](docs/state/PROGRAM-12M.md)

**Uczciwość:** 1.2 = buy+sell na jednym wierszu + `margin(buy, sell)` w kodzie + `/charges`. Nie accept HITL. U-routes-breadth = jedna trasa operatora, **nie** Exit Wave FE. Isolation RLS = CI (lokalnie PG wisiał). Leftover ≠ DONE. echo ≠ DoD.

**Plan:** [docs/PLAN-REALIZACJA.md](docs/PLAN-REALIZACJA.md)

**2026-09-01:** 1.2 — `charge` buy+sell, marża w kodzie M-08.
