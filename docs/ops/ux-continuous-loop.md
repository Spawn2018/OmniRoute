# PROC-UXCL — ciągła pętla UX/UI (jedna procedura)

| Pole | Wartość |
|---|---|
| ID | **PROC-UXCL** (nadrzędna; w UXCL była PROC-UXCL-08) |
| Wersja | **1.8 — 2026-09-16** |
| Owner | człowiek (CEO / owner produktu) |
| Agent | `ux-loop-orchestrator` (po instalacji); do instalacji — człowiek albo Ask |
| Docelowo w repo | `docs/ops/ux-continuous-loop.md` — **tylko po D2 + `/noc` idle** |
| Status | BADANIA — nie next-ID |

Szablony: `szablony/SIGNAL.md`, `EXPERIMENT.md`, `CLOSURE.md`. Instalacja do repo: `INSTALL-UXCL.md` (nie ta procedura). Job #1: **extract-accept** (D2 w inboxie `czeka`). Context budget: sesja firmy; plaster nie wczytuje `22`–`24` / OS badań / `IDLE-SESJA`. UXCL ≠ fabryka. Po idle UXCL jedzie **w** P-Y (krok INSTALL), nie jako drugi tydzień.

---

## 1. Definicja sukcesu

Pętla jest zamknięta wtedy i tylko wtedy, gdy cykl kończy się **dowodem**:

```
Sygnał → Hipoteza → Zmiana (plaster/RITE) → Weryfikacja (metryka + guardrail)
  → Decyzja ship/iterate/rollback → Closure (benefit_ledger HITL i/lub Plat-HD) → następny sygnał
```

Nie jest pętlą: 50 ekranów bez eventów; heatmapa bez hipotezy; flaga „A/B” bez karty; SUS całej appki; scoring operatora; auto-L3.

Kotwice: HEART×job (Rodden et al.); RITE (Medlock et al.); Kohavi 2020; SRE error budget; flags ≠ experiments; Art.14 oversight.

---

## 2. Warunki startu (każdy tydzień)

1. Przeczytaj `docs/state/CURRENT.md` i lokalne `docs/state/NOC-LIVE.md` (gitignore).
2. Jeśli `status: busy` albo trwa `/noc` → **stop pisania produktu**. Wolno: Signal/Experiment Card w `D:\OMNIROUTE-badania`.
3. WIP hipotez Top 5 ≤ 5. Powyżej → tylko zamykanie, zero nowych w Top 5.
4. Error budget spalony (p95 / 5xx / LCP / bundle — gdy macie liczby) → tylko fix/rollback.
5. Next-ID produktu **nie** pochodzi z tej procedury.
6. Error budget fabryki: `ERROR-BUDGET-POLICY.md` § A — **żywy**. Twarde spalenie → stop Top 5 i stop hire. Tenant G1 = N/A.
7. Noc z problemem: AAR (`szablony/AAR.md`). Trigger A2: PM-FAC, nie sam AAR.
8. Czerwony gate: `szablony/ANDON.md` (`factory_recover`). 3× fail ≠ nowy skill.
9. Pulse DORA: nie z tej procedury w `/noc`. Po idle: P-R + P-S (WBR). Nie myl HEART jobu z `factory_df`.
10. G0/unpark nie z tej procedury — `MECHANISMS.md` / PRR.
11. Nauka produktu (Closure) ≠ nauka fabryki (`LEARNING-OS`). Recurrence fabryki nie jest KPI jobu.

---

## 3. Kroki tygodnia

### P1 — Triage (poniedziałek, 30–45 min)

Wejście: PostHog (gdy L1 żyje) albo tarcia z HHL / Plat-HD / reject extract / fail CI. Agreguj per **extract-accept**, dopóki D2 nie wskaże jobu #2.

Wyjście: 0–5 Signal Cards; reszta `parked` z powodem.

Reguły: agreguj per **job GLOSSARY**, nie per osoba. Defect → Plat-HD defect; tarcie → `ux_friction`. Zakaz KPI karnych.

Bez eventów jobowych: triage z obserwacji / diary / rejectów — i **jedna** propozycja leftover do PLAN (D2 człowieka), nie plaster „bo UXCL”.

### P2 — Privacy przed instrumentacją (gdy rusza event/replay)

Skill: `ux-privacy-instrument`.

Checklist (wszystkie TAK albo stop):

- [ ] Cel pomiaru zapisany (purpose limitation)
- [ ] Consent / opt-in na eventy
- [ ] Mask inputs (hasła, NIP w polach, sekrety)
- [ ] Cookieless / person profiles świadomie
- [ ] Replay **osobna** zgoda albo wyłączony
- [ ] Zero scoringu osoby w nazwach i payloadzie
- [ ] Nazwy eventów z GLOSSARY — start: extract-accept (nie dwa joby)

Zakaz: FullStory/heatmap bez hipotezy+DPIA; vanity pageview jako primary.

### P3 — Hipoteza

Mała zmiana UI → RITE (task, nie „poklikaj”).  
Wymaga dowodu A/B → skill `ux-experiment-steward` (Experiment Card) **zanim** flaga.  
Wymaga kodu produktu → CURRENT → `/plan-modul` albo `/plaster`. Nie omijaj kolejki.

Rozdział: `flag_*` = release; `exp_*` = nauka. Nie „włączymy flagę i zobaczymy”.

### P4 — Zmiana

Jeden pisarz. `lowca-duplikatow` przed nową funkcją. HITL / RLS / OpenFGA jak każdy plaster. Owner accept na „naprawę UX od agenta” (Plat-HD), zanim merge poza `/noc` kolejki.

### P5 — Weryfikacja

Primary = job (czas, drop, accept/modify/reject). Guardrail = p95 albo error budget albo accept-rate. SUS tylko **task-based** (Brooke). UMUX-Lite / SEQ wolno jako tańszy pulse.

### P6 — Decyzja

`ship` / `iterate` / `rollback`. Spalony budget = brak nowego feature.

### P7 — Closure (piątek)

Closure Card. `benefit_ledger` = HITL insert (nie SQL z `charge`). Plat-HD close/reject przez człowieka. Orchestrator: liczby otwarte / zamknięte / park; kolizje × `/noc` = **0**.

### P8 — AI (asynchronicznie)

Przed releasem extract/modelu: golden + human label; Art.14 (override, nie rubber-stamp). Zakaz żywego OpenAI w CI (Park CURRENT). Zakaz zapisu L0–2 z modelu.

---

## 4. Macierz uprawnień

| Akcja | Agent | Człowiek |
|---|---|---|
| Signal / Experiment / Closure w badaniach | D0 | D1 czytaj |
| Eventy / plaster FE | plan + kod po D2 lub `/noc` na CURRENT | leftover do PLAN |
| Instalacja skill/proc do repo | nie | D2 |
| Owner approve Plat-HD | propozycja | D2 |
| Sekrety, IdP, unpark live | nie | D2 |
| Auto-L3 / scoring osoby / Mission Control | zakaz | zakaz |

---

## 5. Meta-KPI zdrowia pętli (nie vanity)

| Metryka | Cel | Alarm |
|---|---|---|
| Signal → Closure w ≤14 dni | większość Top 5 | karty bez daty stop |
| Kolizje agent × `/noc` | 0 | > 0 |
| Experiment bez guardrail | 0 | > 0 |
| Plat-HD bez owner decyzji | < 10% otwartych | wiszące propozycje |
| Event z PII | 0 | natychmiast stop instrumentacji |

---

## 6. Stop

- `/noc` busy → zero zapisu w drzewie OmniRoute z tej procedury.
- Brak L0 przy nowych eventach → stop instrumentacji.
- Katalog 205 pozycji **nie** jest backlogiem tygodnia. Orchestrator bierze max 1 klasę M/X z P0 UXCL.
- Sesja `/plaster`/`/noc` nie wczytuje tej procedury jako next-ID ani `24`.
