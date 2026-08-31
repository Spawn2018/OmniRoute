# U-palette-ops — ⌘K akcje operatora

**Status:** archived 2026-09-01  
**Moduł:** UI shell  
**Spec:** PROGRAM-12M standing #9 · Exit Wave FE U-palette-ops

## Zakres

- Paleta ⌘K: grupa **Akcje operatora** — extract, accept-focus, save-view, clear-session
- extract / accept-focus → `/extractions` + zdarzenie (klik ekstrakcji / focus Akceptuj)
- save-view → zapis widoku DataTableShell (nazwa `operator` gdy pusta)
- clear-session → istniejące `clearSessionToken()` (bez API sesji / Auth0)
- Vitest: paleta bez czterech akcji = fail

## Poza zakresem

rewrite session/Auth0, Exit Wave FE

## Post-plaster

| Pytanie | Werdykt | Notatka |
|---|---|---|
| Skuteczność | PRZESZŁO | ⌘K ma akcje, nie tylko nawigację |
| Szybkość | N/A ten plaster | paleta, nie budżet p95 |
| Dług w diffie | OK | katalog + subscribe; bez nowej warstwy API |
| Docs/OS | PRZESZŁO | CURRENT = U-density; nie Exit Wave FE |
