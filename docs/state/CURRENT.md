# Bieżący focus

**Faza:** kolejka Q1 — M-05 Geografia, plaster **4.0** `port`  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **3.0** M-03 `organization_setting` (zarchiwizowany)  
**Etap:** **Plaster** (delta 4.0 zaakceptowana). Nowa rozmowa Agent + `/plaster`.  
**Następny:** **4.0** M-05 `port` + seed `cristan/improved-un-locodes` + `resolve` (Gdingen→PLGDY) + `/ports`. Delta: `docs/deltas/open/4.0-port.md`. Spec: `docs/spec/geography.md`. Nie 4.1/4.2. Nie Q2.  
Q1.1 = 4.1 `location`+strefy (najpierw Plan). Q1.2 = 4.2 `terminal`+WPI (Plan). Q2 = M-10 **po** 4.2. M-02 **parked**. Auth0 **odroczone**. Exit Wave FE **nie** claim.

**Poza kolejką Q (nie startuj zamiast 4.0):** ADR-0003 + makiety `docs/design/`. Leftovery UI: `U-oklch-dark`, `U-money-align`, `U-condensed`, `U-primitives-json`, `U-i18n-structure`, `U-playwright-axe`, `U-print`. Watchtower/mapa dopiero po M-05 i Fali 5.

**Spec (jedna na sesję):** `docs/spec/geography.md` · delta `docs/deltas/open/4.0-port.md`

**Kanon:** [docs/PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — jedyny plan, § Kolejka realizacji.

**Uczciwość:** 3.0 na origin. Żywe M-07 = `rate_line`, żywe M-08 = `charge` — nie nadpisuj numerami archiwum M-07/M-08. HITL zostaje. ExtractionService nie importuje rates. LLM nie liczy. `port.organization_id` obowiązkowy (nie NULL z archiwum).

**2026-09-01:** Plan Q1 zaakceptowany. M-05 = 4.0 → 4.1 → 4.2, potem Q2. Audyt UI → ADR-0003 (dokument + canvas, zero `frontend/`).
