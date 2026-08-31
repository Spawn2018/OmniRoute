# U-a11y — ścieżka klawiatury + focus-visible

**Status:** archived 2026-09-01  
**Moduł:** UI shell  
**Spec:** PROGRAM-12M Exit Wave FE U-a11y · ADR-0002

## Zakres

- Globalne `:focus-visible` (outline token `--ring`)
- Skip link „Przejdź do treści” → `#main-content`
- Sidebar, paleta, toolbar tabeli, HITL Accept/Reject w ścieżce Tab / ⌘K
- Vitest: brak `:focus-visible` albo brak skip/HITL button = fail
- RTL samo nie zamyka plastra

## Poza zakresem

Exit Wave FE, nowy design system

## Post-plaster

| Pytanie | Werdykt | Notatka |
|---|---|---|
| Skuteczność | PRZESZŁO | focus-visible + skip + HITL w Tab |
| Szybkość | N/A ten plaster | a11y, nie budżet p95 |
| Dług w diffie | OK | token ring, bez nowej biblioteki |
| Docs/OS | PRZESZŁO | CURRENT = U-size-limit-real; nie Exit Wave FE |
