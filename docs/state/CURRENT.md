# Bieżący focus

**Faza:** leftover produktu / fabryka modułów  
**Repo:** https://github.com/Spawn2018/OmniRoute  

**Ostatni plaster:** **2.0** M-21 quotation SQL z istniejącego `rate_line` (zarchiwizowany)  
**Następny:** M-03 konfiguracja jako dane (`MODULES.md`) — job operatora. Auth0 I1/I2 **odroczone** — brak tenanta; nie pytać. Sesja = email+hasło+JWT. Exit Wave FE **nie** claim. Outbox (M-02) nie startować bez zdarzeń między modułami.

**Spec (jedna na sesję):** wskaż spec z `MODULES.md` przy starcie plastra.

**Kanon:** [docs/state/PROGRAM-12M.md](docs/state/PROGRAM-12M.md)

**Uczciwość:** 2.0 na origin. U-* ID na origin — Exit Wave FE **nie** claim. 0.12/0.15 = session email+hasło+JWT, **nie** IdP. Auth0 I1/I2 nie ruszane (brak tenanta — zero kodu Auth0). HITL zostaje. ExtractionService nie importuje rates/quotations. Accept→`rate_line` zostaje w API.

**Plan:** [docs/PLAN-REALIZACJA.md](docs/PLAN-REALIZACJA.md)

**2026-09-01:** 2.0 zamknięty. Następny kod = M-03 config-as-data.
