# U-art50 — label „propozycja AI” na draftach HITL

**Status:** archived 2026-09-01  
**Moduł:** M-20 UI  
**Spec:** PROGRAM-12M § Exit Wave FE · Art. 50 = UI, nie PDF prawny

## Zakres

- Widoczny label `propozycja AI` na recenzji szkicu HITL (`data-generated-content="ai"`)
- Pusty stan kolejki bez labelu
- Vitest: markup szkicu bez labelu = fail

## Poza zakresem

copilot/mail (gdy polecą), PDF prawny, Auth0, Exit Wave FE

## Post-plaster

| Pytanie | Werdykt | Notatka |
|---|---|---|
| Skuteczność | PRZESZŁO | draft UI ma label; empty nie |
| Szybkość | N/A ten plaster | jeden string w recenzji |
| Dług w diffie | OK | helper + markup; bez nowej warstwy |
| Docs/OS | PRZESZŁO | CURRENT = U-palette-ops; nie Exit Wave FE |
