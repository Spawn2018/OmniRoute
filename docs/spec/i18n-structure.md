# U-i18n-structure — klucze pl i format locale

**Leftover żywy:** U-i18n-structure (PLAN § Wave FE, token `ui_message`, nie tabela)  
**Plaster:** **55.0** (plan)  
**Status:** operator **widzi** polskie napisy z katalogu kluczy na `/quality` i `/rollout`. Jeden język w paczce. Nie drugi język. Nie nowa tabela.

Delta: [docs/deltas/open/55.0-i18n-structure.md](../deltas/open/55.0-i18n-structure.md).

## 55.0 `t()` + `formatInstant`

### Zakres

- Katalog `pl` i `t(key)` w `frontend/src/lib/i18n.ts` — bez i18next
- `formatInstant` przez `Intl.DateTimeFormat("pl-PL")` na ISO; nie `Number` na kwocie
- Nagłówki `/quality` i `/rollout` przez `t()` (gate: hardcoded na **nowym** ekranie)
- Test pinu kluczy i formatu
- Zero nowej tabeli i trasy

### Poza 55.0

Migracja wszystkich katalogów · EN · grouping tysięcy na `<Money/>` · Playwright

### HC

- Marża zostaje w `charge`.
- LLM nie liczy.
- HITL zostaje.
- Kwota zostaje stringiem z 52.0 — locale nie woła `parseFloat` / `Number`.
