# U-playwright-axe — trzy ścieżki E2E + axe

**Leftover żywy:** U-playwright-axe (PLAN § Wave FE, token `e2e_axe_route`, nie tabela)  
**Plaster:** **56.0** (zamknięty)  
**Status:** CI i `just gate` palą brak Playwright i axe poza CI. Nie nowa tabela. Nie live accept HITL.

Delta: [docs/deltas/archived/56.0-playwright-axe.md](../deltas/archived/56.0-playwright-axe.md).

## 56.0 Playwright chromium + axe na trzech trasach

### Zakres

- `@playwright/test` + `@axe-core/playwright`, tylko Chromium
- Trzy ścieżki: `/session` → `/rate-lines`; `/extractions`; `/quotations`
- axe na każdej; `just frontend-e2e` **po** `perf`
- CI: instalacja Chromium przed `code-gate`
- Zero nowej tabeli i trasy; zero kliknięcia Akceptuj bez szkicu

### Poza 56.0

U-print · Firefox/WebKit · live login + accept HITL (API+seed)

### HC

- Marża zostaje w `charge`.
- LLM nie liczy.
- HITL: brak optimistic accept w teście.
- Kwota nie przez `parseFloat`.
