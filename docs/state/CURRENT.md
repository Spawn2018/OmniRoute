# Bieżący focus

**Faza:** Auth0  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **1.3** accept → `rate_line` (zarchiwizowany)  
**Następny:** **Auth0 I1** BFF + PKCE + cookie. Charge 1.3 DONE. Wave FE U-* nadal otwarte (nie startowane tu). 0.24 pip-audit pominięty (opcjonalny).

**Spec (jedna na sesję):** [docs/state/PROGRAM-12M.md](docs/state/PROGRAM-12M.md) Auth0 I1

**Kanon:** [docs/state/PROGRAM-12M.md](docs/state/PROGRAM-12M.md)

**Uczciwość:** 1.3 = accept HITL + `rate_line` (kupno) w jednej transakcji HTTP, orchestracja API. `ExtractionService` nie importuje rates. Nie `charge`/sell z LLM. Nie outbox. U-routes-breadth = link na HITL + istniejące `/rate-lines`, **nie** Exit Wave FE. Isolation/integration = CI (lokalnie PG wisiał). Leftover ≠ DONE. echo ≠ DoD.

**Plan:** [docs/PLAN-REALIZACJA.md](docs/PLAN-REALIZACJA.md)

**2026-09-01:** 1.3 — accept zapisuje `rate_line` w jednej transakcji HTTP.
