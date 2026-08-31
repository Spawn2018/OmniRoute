# U-density — compact + toggle na wszystkich listach

**Status:** archived 2026-09-01  
**Moduł:** UI DataTableShell  
**Spec:** PROGRAM-12M Exit Wave FE U-density

## Zakres

- Domyślna gęstość `compact` w DataTableShell
- Toggle „Gęstość” (Zwarta / Wygodna) na toolbarze
- Rejestr list: `/tenancy/users`, `/charge-codes`, `/rate-lines`, `/charges`, `/extractions`
- Vitest: brak compact/toggle albo lista tylko users = fail

## Poza zakresem

nowe moduły, Exit Wave FE

## Post-plaster

| Pytanie | Werdykt | Notatka |
|---|---|---|
| Skuteczność | PRZESZŁO | 5 list biznesowych przez ten sam shell + toggle |
| Szybkość | N/A ten plaster | UI gęstości, nie p95 50k |
| Dług w diffie | OK | rejestr + aria-label; bez drugiego table engine |
| Docs/OS | PRZESZŁO | CURRENT = U-a11y; nie Exit Wave FE |
