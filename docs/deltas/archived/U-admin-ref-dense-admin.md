# U-admin-ref — gęsty admin (widoczny UI)

**Status:** archived 2026-09-01  
**Moduł:** UI shell  
**Spec:** PROGRAM-12M Exit Wave FE U-admin-ref · ADR-0002 shadcn-admin wzorce

## Zakres

- Pulpit = tabela jobów operatora (istniejące trasy), nie hello-dashboard / Shell 0.5
- Sidebar compact (`data-admin-ref="sidebar-density"`)
- DataTableShell toolbar (`table-toolbar`)
- Header ⌘K = akcje (`command-actions`)
- Vitest: hello copy albo brak powierzchni = fail

## Poza zakresem

70 pustych M-xx, Exit Wave FE (U-routes-breadth jeszcze otwarte w momencie pisania)

## Post-plaster

| Pytanie | Werdykt | Notatka |
|---|---|---|
| Skuteczność | PRZESZŁO | UI gęsty; nie checklista markdown-only |
| Szybkość | N/A ten plaster | layout, nie p95 |
| Dług w diffie | OK | pulpit bez kafelków; bez fake modules |
| Docs/OS | PRZESZŁO | CURRENT = U-routes-breadth; nie Exit Wave FE |
