# U-size-limit-real — just perf failuje przy przekroczeniu 250 kB

**Status:** archived 2026-09-01  
**Moduł:** ops / FE  
**Spec:** PROGRAM-12M Exit Wave FE U-size-limit-real · AGENTS.md budget gzip initial JS < 250 kB

## Zakres

- `just perf` = `pnpm build` + `check_initial_js_size.py` (nie echo)
- Initial JS = skrypty z `dist/index.html` (gzip)
- `just gate` woła `perf` — CI pada przy ≥ 250 kB
- Vitest/pytest: fixture oversize = exit 1; recipe echo = fail

## Poza zakresem

k6 p95, vulture, pip-audit (nadal echo)

## Post-plaster

| Pytanie | Werdykt | Notatka |
|---|---|---|
| Skuteczność | PRZESZŁO | oversize pada; obecny initial ~125 kB gzip |
| Szybkość | PRZESZŁO | budget initial JS < 250 kB |
| Dług w diffie | OK | jeden skrypt quality; k6 leftover |
| Docs/OS | PRZESZŁO | CURRENT = U-pdf-spans; nie Exit Wave FE |
