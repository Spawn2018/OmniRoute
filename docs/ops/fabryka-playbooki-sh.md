# Fabryka SH — playbooki, RACI, apetyt (Rejestr 16 IX)

| Pole | Wartość |
|---|---|
| Status | KANON ops (promocja braków materialnych 2026-09-16) |
| Źródło | badania `23` §3–§4 / §8 / P-A…P-Y; `24` A1 cooling |
| Prawo | CURRENT > [rejestr-wdrozenia-16-ix.md](rejestr-wdrozenia-16-ix.md) > ten plik |
| Zakaz | nie next-ID produktu; nie wczytuj `22`–`24` do plaster |

## 1. Apetyt i cooling (Shape Up)

Wartości D2: `1 decyzja` | `1 plaster` | `1 noc` | `1 tydzień` | `park`.  
**Cooling:** D3 odrzucone nie wraca przez **14 dni** bez nowej przesłanki (`24` A1).

Inbox żywy: `D:\OMNIROUTE-badania\DECISION-INBOX.md` (poza gitem).

## 2. Budżet uwagi CEO (`23` §3.1 / CEO-OS)

Cel: ≤5 h decyzji / tydzień + ≤1 h raportów (WBR ≤15 min). Reszta = agenci.  
CEO nie robi: ruff, migracji, recenzji każdego pliku w nocy.

## 3. RACI (skrót `23` §4) — jedno A na decyzję

| Decyzja | A (accountable) | R | C | I |
|---|---|---|---|---|
| Next-ID / Q | CURRENT + człowiek | Planista | — | Nocka |
| Park / unpark live | człowiek D2 | — | Planista | |
| Accept extract | człowiek | — | Extraktor | |
| Gate czerwony | Andon / PM-FAC | Zamykacz | Recenzent | |
| Hire skill | człowiek D2 | — | — | |
| G0 go-live | człowiek + PRR | — | Platforma | |

Krytyk (`pr-review`) **nie** jest A naprawy — mierzy; naprawa = plasterownik.

## 4. Playbooki P-A…P-Y (indeks → szablon)

| ID | Nazwa | Szablon / ops | Kiedy |
|---|---|---|---|
| P-A | Decision Inbox | badania `DECISION-INBOX.md` | ciągle |
| P-B | INSTALL UXCL | było; **DONE** 3 skille + PROC | nie powtarzaj |
| P-R | FACTORY-PULSE | [`szablony/FACTORY-PULSE.md`](szablony/FACTORY-PULSE.md) | w P-Y |
| P-W | CRAFT-PULSE | [`szablony/CRAFT-PULSE.md`](szablony/CRAFT-PULSE.md) | w P-Y |
| P-X | SKILLS-PULSE | [`szablony/SKILLS-PULSE.md`](szablony/SKILLS-PULSE.md) | w P-Y |
| P-V | Recurrence flush | [`szablony/RECURRENCE.md`](szablony/RECURRENCE.md) | w P-Y |
| P-S | WBR | [`szablony/WBR.md`](szablony/WBR.md) | w P-Y (CEO) |
| P-Y | IDLE-SESJA | [`szablony/IDLE-SESJA.md`](szablony/IDLE-SESJA.md) | po idle; **jedna** sesja |
| P-K | PM-FAC | [`szablony/PM-FAC.md`](szablony/PM-FAC.md) | trigger A2 |
| P-N | PROMPT-CHG | [`szablony/PROMPT-CHG.md`](szablony/PROMPT-CHG.md) | zmiana promptu |
| P-Q | MODEL-CARD | [`szablony/MODEL-CARD.md`](szablony/MODEL-CARD.md) | zmiana modelu |
| — | PREMORT / PRR / LAUNCH | szablony | unpark G0 |
| — | AAR / ANDON / SEV | szablony | noc z problemem / SEV |
| — | SIGNAL / EXPERIMENT / CLOSURE | szablony | pętla UXCL |
| — | FinOps / PARK-RADAR / TOIL | szablony | P-Y / kwartał / miesiąc |
| — | PACK-STOP | [`szablony/PACK-STOP.md`](szablony/PACK-STOP.md) | „ulepsz elite” = D0 |

Nowe `*-OS.md` / P-Z = **zakaz** (PACK-STOP).

## 5. DORA / Dependabot / Fire skill / Radar (kolejka `/noc` = rytuał)

| ID PLAN | Co | Status |
|---|---|---|
| **SH-R16-12** | Pierwszy FACTORY-PULSE z liczbami `gh` (P-Y) | DONE 2026-09-16 |
| **SH-R16-13** | Dependabot: 1 paczka / tydzień WIP=1 (alerts już ON; auto-PR OFF) | czeka idle (zakaz auto-PR w `/noc`) |
| **SH-R16-14** | Audit skill >4 tyg. (fire/archiwum) w P-Y | DONE 2026-09-16 — 0 do fire |
| **SH-R16-15** | PARK-RADAR Q3/Q4 2026 ≤30 min | DONE Q3 2026-09-16 |

Pasmo elite: dopiero po 4 tyg. pulse i n≥8 CFR — nie ogłaszaj wcześniej.

## 6. Diátaxis (docs)

Jeden plaster = jeden spec z CURRENT. How-to operatora ≠ reference API ≠ explanation wizji. Mapowanie: `docs/operator/` (how-to), `docs/spec/` + MODULES (reference), VISION/PLAN (explanation), tutorial = rzadko i świadomie.
