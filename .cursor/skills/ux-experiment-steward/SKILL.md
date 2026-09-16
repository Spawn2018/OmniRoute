---
name: ux-experiment-steward
description: L3/L6 UXCL — Experiment Card, flags≠A/B, primary+guardrail+stop. Nie włączaj flagi bez karty.
---

# ux-experiment-steward

Jeden job: **protokół nauki**. Flaga release ≠ eksperyment.

Kotwica: Kohavi et al., *Trustworthy Online Controlled Experiments* (2020). HEART×job (Rodden et al.). Nie Statsig „bo top SH”.

## Wejście

1. Signal Card (`D:/OMNIROUTE-badania/szablony/SIGNAL.md`) albo jedno zdanie hipotezy od człowieka.
2. CURRENT + NOC-LIVE (busy → tylko karta w badaniach).
3. Stan flag (jeśli PostHog już jest). Brak flag = nie wymyślaj platformy.

## Kroki

1. Wypisz Experiment Card 1 strona (`D:/OMNIROUTE-badania/szablony/EXPERIMENT.md`). Brak primary albo guardrail = **stop**, nie kod.
2. Oznacz osobno:
   - `flag_*` — release / kill-switch
   - `exp_*` — nauka (hipoteza, stop)
3. Primary = metryka **jobu** (czas, drop, accept/modify/reject). Guardrail = p95 albo error budget albo accept-rate.
4. Małe N HHL: napisz wprost sequential albo holdout albo **RITE-only**. Nie udawaj mocy. Nie p-hack.
5. Stop rule: data albo N albo guardrail spalony. Bez stop = nie start.
6. Po stop: `ship` / `iterate` / `rollback` + link Closure Card. Nie zostawiaj flagi „na zawsze jako eksperyment”.
7. Jeśli wynik wymaga kodu produktu → leftover / CURRENT. Ten skill **nie commituje** (krytyk/steward ≠ pisarz).

## DoD

- Karta 1 strona z hipotezą, primary, guardrail, stop, owner.
- `flag_*` ≠ `exp_*`.
- Zero vanity DAU jako primary.

## Zakaz

- „Włączymy flagę i zobaczymy”
- Dwa UI bez protokołu
- Scoring osoby / operatora
- Live A/B jako next-ID z marka `ab_sus`
- Auto-zejście jakości, auto-L3, Mission Control
- Silnik matching / heatmap
- Pisanie na `main` przy `/noc` busy
- Wczytywanie `22`/`23`/`24` do sesji `/plaster`
