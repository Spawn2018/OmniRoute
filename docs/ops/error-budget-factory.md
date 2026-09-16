# Error-budget policy (fabryka)

| Pole | Wartość |
|---|---|
| Wersja | **2.6 — 2026-09-16** (promocja Rejestr 16 IX) |
| Status | **Fabryka: EGZEKUJ.** Tenant G1: N/A do liczb. G0 w parku. |
| Kotwica | SRE (Beyer et al.); badania `DORA-FABRYKA.md`; AGENTS p95; PLAN § Gate (k6 echo ≠ DoD) |
| Kolejka | [rejestr-wdrozenia-16-ix.md](rejestr-wdrozenia-16-ix.md) · SH-R16-1 |

Dwa budżety. **Nie** mieszaj. Spalony budżet fabryki ≠ „spalony SLO HHL”.

---

## A. Fabryka (żywy od dziś)

### A1. Twarde spalenie — tylko Andon / fix / leftover

Zero nowego etatu, zero nowego Signal w Top 5, zero „ulepsz SH w OmniRoute”, dopóki nie zejdzie do zera:

| Sygnał | Próg | Co robisz |
|---|---|---|
| Kolizja agent × `/noc` | > 0 | stop drugiego pisarza; P-J |
| Echo / STUB jako DONE | > 0 | Andon + leftover PLAN; nie zamykaj Q |
| `craft_skip` (tabela skrócona) | > 0 | Andon; pełna tabela albo leftover |
| `craft_floor` (podłoga spadła) | > 0 | przywróć floor; nie `--write` w dół |
| `craft_critic` (recenzent commitował) | > 0 | revert commitu recenzenta; naprawa = Q plastra |
| `skill_extra` / `skill_n` ≠ 10 (13 po INSTALL) | > 0 | archiwum + agentlint; nie „zostaw na później” |
| Event PII | > 0 | stop instrumentacji (incydent) |
| `--no-verify` / force-push | > 0 | PM-FAC (A2); **SEV-1** |
| SEV-1 otwarte | > 0 | stop Signal/hire aż PM-FAC ma 1. akcję |
| Cross-tenant SQL | > 0 | blocker merge (HC) |

### A2. Miękkie spalenie — jedziesz kolejkę, ale jedna dźwignia

| Sygnał | Próg | Co robisz |
|---|---|---|
| `factory_cfr` | > 15% przy n≥8 | P-R; zakaz hire; nie nowy skill |
| `factory_recover` | poza godziną nocy **i** bez leftover | AAR albo PM-FAC |
| D2 otwarte >7 dni | > 0 | CEO zamyka inbox; freeze Signal |
| PM-FAC open >7 dni | > 0 | CEO D2: zamknij albo 1 akcja |
| `factory_rework` | > 0 | traktuj jak twarde jeśli STUB=DONE |
| `learn_recurrence` | ≥ 1 w 28 dniach | dwuobieg; nie nowy skill; nie druga karta |
| `craft_slop_recurrence` | ≥ 1 w 28 dniach | dwuobieg albo leftover `craft_style`; nie AlwaysApply +1 |
| `skill_recurrence` | ≥ 1 w 28 dniach | dwuobieg tekstu SKILL/AGENTS; nie skill #11 |
| `factory_ai_spend` WoW ≥2× przy n≤ | > 0 | P-Y / `FINOPS-NOC.md`; mniej kontekstu lub pisarzy; nie skill |

Źródło tygodnia: jedna `IDLE-SESJA.md` (arkusze FACTORY + CRAFT + SKILLS). Brak P-Y = budżet fabryki **nieznany**, nie „OK”.

---

## B. Tenant (G1+, po liczbach)

Wspólny UI+API. Spalony = tylko fix/rollback, zero nowego feature. Dziś **N/A**.

| Sygnał | Źródło dziś | DoD |
|---|---|---|
| Initial JS gzip | `just perf` — real | < 250 kB (to już gate, nie SLO tenanta) |
| k6 p95 wyceny / API | stub/echo w PLAN | **nie** claim |
| LCP / p95 endpoint | AGENTS | gdy zmierzone na hoście |
| 5xx u tenanta | brak hosta | po G0 |
| Event PII | privacy | 0 (też A1) |

---

## Stop

- Osobne „FE może, BE nie”.
- Echo recipe jako „budget OK”.
- Scoring operatora jako budżet.
- Czerwony CI = „SLO tenanta” przy G0 w parku.
- Cel roku „CFR=0” (Goodhart) — dążenie przez leftover, nie przez ukrywanie faili.
- Czwarty recenzent jako „budżet jakości”.
- Obniżenie `quality_floor` żeby noc była zielona.
- Jedenasty skill fabryki jako „więcej kontroli”.
