# Bieżący focus

**Faza:** C — leftover tenancy  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **0.16 T1** `omniroute_app` NOBYPASSRLS (zarchiwizowany)  
**Następny:** **0.17 T2** matryca RLS S1–S6 + WITH CHECK — nie 0.18 w tym samym PR

**Spec (jedna na sesję):** [docs/spec/tenancy.md](docs/spec/tenancy.md)

**Kanon:** [docs/state/PROGRAM-12M.md](docs/state/PROGRAM-12M.md)

**Uczciwość:** OAuth/OIDC = Auth0 **I1 po Wave A**. Leftover ≠ DONE. echo ≠ DoD.
RLS integration T1 = CI; lokalnie PG wisiał.

**Plan:** [docs/PLAN-REALIZACJA.md](docs/PLAN-REALIZACJA.md)

**2026-09-01:** 0.16 T1 — rola `omniroute_app` NOBYPASSRLS; runtime URL nie jest superuserem.
