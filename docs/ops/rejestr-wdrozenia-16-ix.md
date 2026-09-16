# Rejestr wdrożenia 16 IX — pakiet 20 plików badań

```
status:        KANON KOLEJKI (promocja 2026-09-16)
zrodlo:        D:\OMNIROUTE-badania — 20 plików z datą 2026-09-16
polecenie:     operator — 100% pokrycie; park z warunkiem; reszta w kolejce /noc
prawo:         CURRENT > ten rejestr > PLAN § Fala SH-R16 > pin 2026-09-08c
```

**Cel:** żadna treść z 20 plików nie ginie. Każda pozycja ma status:
`DONE` | `NOW` | `AFTER_527` | `PARK` | `REJECT` | `BADANIA` (konstytucja zostaje na `D:\`, śledzona tu).

**Egzekucja:** `/noc` czyta [CURRENT.md](../state/CURRENT.md). Gdy CURRENT wskazuje
`SH-R16-*`, robi ten wiersz. Gdy wskazuje `527.0+`, jedzie oś produktu.
Pin **2026-09-08c** nie wypada — leftover HITL wraca po domknięciu batchy `NOW`.

Surowiec (nie wczytuj do plastra produktu): `SH-CZYTAJ.md`, `22`–`24`, `*-OS.md`.
Ten plik **jest** kanonem kolejki fabryki z 16 IX.

---

## 0. Pokrycie 20/20 plików

| # | Plik badań | Rola | Stan wdrożenia |
|---|---|---|---|
| 1 | `00-INDEKS.md` | spis + zakaz AI0 | **DONE** (reguły w AGENTS/CURRENT; AI0 odrzucony) |
| 2 | `22-PRZYSPIESZENIE-GO-LIVE-FABRYKA.md` | G0/G1/G2 + OS go-live | **POKRYTE** — G0 PARK; G1 job L1 = AFTER_527; Fala 0 UXCL DONE |
| 3 | `23-PLAN-SOFTWARE-HOUSE.md` | konstytucja firmy | **POKRYTE** — prawo w AGENTS; rytuały = BADANIA+P-Y; etaty = skills |
| 4 | `24-ROZWOJ-SOFTWARE-HOUSE.md` | backlog firmy A1–A16 / E1–E8 | **POKRYTE** — A1/INSTALL DONE; E4–E8 PARK; artefakty przy triggerze |
| 5 | `CEO-OS.md` | aneks CEO | **POKRYTE** — D2 extract-accept akceptuję; WBR ograniczenie DONE w nocna |
| 6 | `CRAFT-OS.md` | łańcuch rzemiosła | **DONE** (haki + L1–L3 no-slop); pulse = P-Y |
| 7 | `DECISION-INBOX.md` | inbox D2/D3 | **BADANIA** (żywy poza gitem); decyzje 16 IX wpisane tu jako DONE/PARK |
| 8 | `DORA-FABRYKA.md` | analogi `factory_*` | **POKRYTE** — `gate=success` DONE; pulse 4 tyg. = NOW/P-Y |
| 9 | `ERROR-BUDGET-POLICY.md` | Andon fabryki | **DONE** (`ops/error-budget-factory.md`) |
| 10 | `GIGANT-LUKI-2026.md` | 6 luk IX 2026 | **POKRYTE** — ruleset+alerts DONE; szablony GITHUB/EAA/HIRE/SUPPLY w ops; SBOM/attestation/hire PARK |
| 11 | `INSTALL-UXCL.md` | 3 skille + PROC | **DONE** |
| 12 | `JAK-PISZEMY.md` | semantyka / komentarz / Diátaxis | **DONE** L1–L3 + Diátaxis w `fabryka-playbooki-sh.md` |
| 13 | `JAK-PISZEMY-AUTOMACJA.md` | podłoga haków; L4 PARK | **DONE** L1–L3; L4/L5 = PARK/REJECT |
| 14 | `JAK-PISZEMY-RESZTA.md` | test/parse/debug | **DONE**; MagicMock L5 PARK |
| 15 | `LEARNING-OS.md` | recurrence + kubełki | **POKRYTE** — friday + SLA 7 dni; flush = P-Y |
| 16 | `MECHANISMS.md` | PRR/WBR/SEV/LAUNCH | **POKRYTE** — szablony w ops; G0 PARK |
| 17 | `PROC-UXCL.md` | pętla UX | **DONE** (kanon + szablony SIGNAL/EXPERIMENT/CLOSURE); job = UXCL-L1 |
| 18 | `SH-CZYTAJ.md` | spis + zakaz w plasterze | **BADANIA** + enum w `context.mdc` |
| 19 | `SKILLS-OS.md` | 10+3 skilli | **DONE**; fire >4 tyg. = SH-R16-14 |
| 20 | `ZRODLA-FABRYKA.md` | bibliografia | **BADANIA** (nie rytuał) |

Szablony: **29/29** w `docs/ops/szablony/`. Playbooki/RACI: [fabryka-playbooki-sh.md](fabryka-playbooki-sh.md).

---

## 1. Kolejka `/noc` (twarda kolejność)

### 1.1 Batch NOW — bez parkowania (przed dalszym HITL albo w pierwszej nocy)

| ID | Co | Tryb | Status | Poza zakresem |
|---|---|---|---|---|
| **SH-R16-0** | Ten rejestr + wiersz PLAN § Fala SH-R16 + CURRENT | docs | **DONE** | nie 527.0 kod |
| **SH-R16-1** | Polityka error-budget fabryki → `docs/ops/error-budget-factory.md` | docs | **DONE** | nie SLO tenanta |
| **SH-R16-2** | Karta wiedzy PM-FAC W38 → `docs/_knowledge/memory-patterns/pm-fac-20260916.md` | docs | **DONE** | nie nowy OS |
| **SH-R16-3** | Szablony → `docs/ops/szablony/` (**29/29**, w tym SIGNAL…HIRE) | docs | **DONE** 2026-09-16b | kopiuj przy zdarzeniu |
| **SH-R16-4** | Leftover PLAN: **UXCL-L1** eventy jobu extract-accept | leftover wiersz | **DONE** (wiersz w PLAN) | kod = AFTER_527 |
| **SH-R16-5** | Leftover PLAN: **AI3-payload** | leftover wiersz | **DONE** (wiersz w PLAN) | żywy OpenAI CI = PARK |
| **SH-R16-6** | Audit GH Actions | chore | **DONE** | brak `pull_request_target` |
| **SH-R16-7** | Wiersz `factory_ai_spend` w WBR | docs | **DONE** | CEO wkleja $ |
| **SH-R16-8** | False DONE: PROC kanon; PACK-STOP; SLA 7d; enum context budget | docs | **DONE** 2026-09-16b | — |
| **SH-R16-9** | Materialne: playbooki/RACI/cooling/CEO/Diátaxis | docs | **DONE** (`fabryka-playbooki-sh.md`) | — |
| **SH-R16-10** | Rejestr gap R16 + statusy | docs | **DONE** 2026-09-16b | — |
| **SH-R16-11** | Meta-KPI Closure ≤14d w PROC | docs | **DONE** 2026-09-16b | egzekucja po UXCL-L1 |
| **SH-R16-12** | FACTORY-PULSE pierwsze liczby | rytuał P-Y | **czeka** | idle + P-Y |
| **SH-R16-13** | Dependabot 1 paczka / tydzień | rytuał idle | **czeka** | nie auto-PR w nocy |
| **SH-R16-14** | Fire skill >4 tyg. | rytuał P-Y | **czeka** | friday / IDLE |
| **SH-R16-15** | PARK-RADAR Q3/Q4 2026 | rytuał kwartał | **czeka** | idle ≤30 min |

Po **SH-R16-8…11** (docs): `/noc` produkt = **527.0**, potem UXCL-L1/AI3. Rytuały **12–15** = gdy idle/P-Y (nie skip — wiersz w PLAN).

### 1.2 AFTER_527 — produkt (oś pinu + job G1)

| ID | Co | Status | Warunek startu |
|---|---|---|---|
| **527.0+** | `margin_floor` HITL → dalsza oś CURRENT | czeka (CURRENT) | po batch NOW albo równolegle gdy CURRENT tak wskaże |
| **UXCL-L1** | Eventy `extract_*` + privacy checklist; job extract-accept mierzalny | PARK→unpark | SH-R16-4 wiersz + L0 privacy TAK |
| **AI3-payload** | Sygnał uczenia extractu | PARK→unpark | SH-R16-5; nie live model CI |
| **Plat-HD-flow** | Obieg ticket→propozycja→owner (nie sam mark) | PARK | G0+G1 + D2 owner |
| **U-\*** | Wave FE standing / Exit nie claim | leftover U | nie next z badań |

### 1.3 PARK — z warunkiem (w planie, nie skip)

| ID | Treść z badań | Warunek unparku |
|---|---|---|
| **G0** | Host + IdP (S53 live) + Cloudflare Access + domena | nowy klient → PREMORT → PRR → LAUNCH → D2 sekrety |
| **G0-env** | GH Environments / attestation / Cosign / SLSA | G0 ma obraz/host |
| **SBOM** | CycloneDX\|SPDX z lockfile (Ask) | idle Ask; nie required check |
| **CodeQL-upload** | SARIF upload na public | decyzja po idle (TO_VERIFY) |
| **EAA** | Claim zgodności / WCAG program | G0 PRR + prawnik; dziś park claimu |
| **CRA** | Manufacturer / SRP | opinia prawna; dziś ścieżka SEV-1 |
| **Hire-human** | Etat człowiek CS→IdP→pieniądz | D3 gdy próg G0\|L1+4 WBR |
| **Hire-PR** | Required PR +1 review | po 1. człowieku |
| **E4–E8** | Dalsze etaty UX/eval z `24` | po żywym L1 albo G0 |
| **Job#2-charge** | Drugi job HEART | po żywym L1 extract-accept |
| **L4-glossary-script** | Detector identyfikator vs GLOSSARY | decyzja D2 — park domyślny |
| **L5-MagicMock** | Regex MagicMock w craft_style | decyzja D2 — park |
| **Hypothesis/mutmut** | HOLD poza DoD | poza osią |
| **DocLayNet / Instructor wiring** | z CURRENT Park | CURRENT wskaże |
| **22-dostępy live** | bez bramy | AI5 + CURRENT |

### 1.4 REJECT — nigdy (świadomie z 20 plików)

11. skill fabryki · Temporal/Hatchet dla fabryki · Infisical · Culture Deck / 16 LP / OKR≠CURRENT · DiRT/chaos · Mission Control · auto-merge / auto-accept extract · L3 write · scoring operatora · required PR solo trunk · Dependabot auto-PR przy `/noc` busy · second AI0 · dump `22`–`24` do plaster · claim elite z n&lt;8 · claim EAA/SLSA z papieru · FRIDAY-OS / CODE-OS / COMMANDS-OS · E3 postmortem-steward skill · 40 agentów w `.cursor/agents/`.

---

## 2. Indeks R16 (100% pozycji z inwentaryzacji)

Każdy wiersz = jedna dyskretna treść. Status: D=DONE, N=NOW, A=AFTER_527, P=PARK, R=REJECT, B=BADANIA.

### 2.1 `00-INDEKS.md`

| ID | Treść | St |
|---|---|---|
| R16-001 | Zakaz drugiego AI0 (`source_ref` jest) | R |
| R16-002 | Next-ID tylko CURRENT | D |
| R16-003 | `12-FALA-AI-KOLEJKA` SUPERSEDED | R |
| R16-004 | skills-draft → UXCL zainstalowane | D |
| R16-005 | Promocja tylko stop `/noc` + jawne polecenie | D |
| R16-006 | Audyt main unprotected — nadpisane rulesetem | D |

### 2.2 `22-PRZYSPIESZENIE-GO-LIVE-FABRYKA.md`

| ID | Treść | St |
|---|---|---|
| R16-010 | Status badań; nie next-ID | B |
| R16-011 | Rola CEO vs agenci; zakaz auto-merge/accept/L3 | D |
| R16-012 | G0 Auth0/CF/domena | P |
| R16-013 | G1 critical path HHL | A |
| R16-014 | Unpark G0 bez PRR = zakaz | P |
| R16-015 | REJECT silniki/Mission Control/11 skilli/skan 70 | R |
| R16-016 | Kolejność G0→G1→extract→silniki→live | P |
| R16-017 | k6 echo ≠ DoD | N |
| R16-018 | Jedno payload extractu AI3 | A |
| R16-019 | PostHog/DPIA/eventy jobu | A |
| R16-020 | Plat-HD obieg | P |
| R16-021 | Wave FE Exit nie claim | A |
| R16-022 | Fala 0 UXCL 3+PROC | D |
| R16-023 | Klasy D0–D3 + inbox | B |
| R16-024 | REJECT Temporal fabryki / cron D1 | R |
| R16-025 | Pętle UXCL w ops | D |
| R16-026 | Fale 1–3 UXCL po L0 | P |
| R16-027 | G0 park do klienta | P |
| R16-028 | Job L1 extract-accept | A |
| R16-029 | TO_VERIFY AI Act / A/B N=HHL | P |

### 2.3 `23-PLAN-SOFTWARE-HOUSE.md`

| ID | Treść | St |
|---|---|---|
| R16-040 | 10 kryteriów sukcesu firmy | N |
| R16-041 | Nie-misja 205/silniki/scoring | R |
| R16-042 | Prawo 1–12 = AGENTS/GROUNDING | D |
| R16-043 | Context budget pkt 13 — enum w `context.mdc` | D |
| R16-044 | Krytyk nie commituje | D |
| R16-045 | PROMPT-CHG + golden | P |
| R16-046 | PM-FAC / AAR | N |
| R16-047 | Hire freeze | B |
| R16-048 | INSTALL UXCL | D |
| R16-049 | OS badań (DORA…PACK) | B |
| R16-050 | Dwa foldery + promocja jawna | D |
| R16-051 | GIGANT pkt 27 | D/P |
| R16-052 | Czarna lista multitask | D |
| R16-053 | Katalog etatów / skills | D |
| R16-054 | Wyłączone automacje | D |
| R16-055 | D2 park G0/Plat-HD/model CI | P |
| R16-056 | Job L1 + job#2 później | A/P |
| R16-057 | Kalendarz Pn–Pt / TOIL / radar | N |
| R16-058 | Inbox >7 → stop Signal | B |
| R16-059 | Playbooki P-R…P-Y | N |
| R16-060 | Hire skill 6 warunków | D |
| R16-061 | Metryki factory_* | N |
| R16-062 | Luki k6/domena/AI3/Plat-HD/FinOps | N/A/P |
| R16-063 | REJECT Temporal/Infisical/required PR | R |
| R16-064 | Plan 90 dni firmy | N |
| R16-065 | Onboarding prompt 18 pkt | B |
| R16-066 | Stała lista REJECTED §17 | R |

### 2.4 `24-ROZWOJ-SOFTWARE-HOUSE.md`

| ID | Treść | St |
|---|---|---|
| R16-070 | Artefakt→klauzula→etat; WIP 1 PM-FAC | N |
| R16-071 | A1 apetyt DONE | D |
| R16-072 | A2–A8 szablony przy triggerze | N |
| R16-073 | A9–A16 kontrakty DONE w badaniach | B |
| R16-074 | Karty `_knowledge` po close | N |
| R16-075 | REJECT CoT/DSPy/40 ról/LLM-judge | R |
| R16-076 | E1 DONE; E3 never; E4–E8 park | D/R/P |
| R16-077 | Automatyzuj toil; nie accept/merge | D |
| R16-078 | Fale A–L firmy | N/A/P |

### 2.5 `CEO-OS.md`

| ID | Treść | St |
|---|---|---|
| R16-080 | Zakres CEO | B |
| R16-081 | Extract-accept akceptuję | D |
| R16-082 | skill_n=13 | D |
| R16-083 | Ograniczenie W38 gate=success | D |
| R16-084 | Ochrona main | D |
| R16-085 | FinOps WBR; hire D3 | N/P |

### 2.6 `CRAFT-OS.md`

| ID | Treść | St |
|---|---|---|
| R16-090 | Łańcuch 10 warstw | D |
| R16-091 | „Jak człowiek” = no-slop | D |
| R16-092 | craft_* pulse P-Y | N |
| R16-093 | Recurrence → karta/dwuobieg | N |
| R16-094 | Zakaz 4. recenzent / floor / CODE-OS | R |

### 2.7 `DECISION-INBOX.md`

| ID | Treść | St |
|---|---|---|
| R16-100 | Job#2 charge po L1 | P |
| R16-101 | G0 czeka na klienta | P |
| R16-102 | INSTALL wykonane | D |
| R16-103 | JAK-PISZEMY L1–L3 | D |
| R16-104 | Ruleset + alerts + scanning | D |
| R16-105 | Pakiet D2 SH akceptuję | B |
| R16-106 | PACK-STOP | B |
| R16-107 | PM-FAC → karta wiedzy | N |
| R16-108 | Hire freeze progi | B |

### 2.8 `DORA-FABRYKA.md`

| ID | Treść | St |
|---|---|---|
| R16-110 | Mierz factory_*; jedno ograniczenie | N |
| R16-111 | Deploy = gate=success | D |
| R16-112 | Close≠deploy w nocna | D |
| R16-113 | Wzory df/lt/cfr + pasma | N |
| R16-114 | Twarde zera | D |
| R16-115 | 90 dni pulse; tenant DORA po G0 | N/P |
| R16-116 | Stop Goodhart / false elite | R |

### 2.9 `ERROR-BUDGET-POLICY.md`

| ID | Treść | St |
|---|---|---|
| R16-120 | A1 twarde spalenie | D |
| R16-121 | A2 miękkie | D |
| R16-122 | Budżet tenanta N/A | P |
| R16-123 | Stop FE/BE osobno / scoring / 11 skill | R |

### 2.10 `GIGANT-LUKI-2026.md`

| ID | Treść | St |
|---|---|---|
| R16-130 | Dependabot alerts ON; updates OFF | D |
| R16-131 | 1 paczka Dependabot / tydzień idle | N |
| R16-132 | SBOM Ask | P |
| R16-133 | Attestation G0 | P |
| R16-134 | CodeQL upload TO_VERIFY | P |
| R16-135 | Ruleset main-factory | D |
| R16-136 | Secret scanning / push protection | D |
| R16-137 | Environments / required PR | P |
| R16-138 | EAA park claim | P |
| R16-139 | CRA TO_VERIFY | P |
| R16-140 | factory_ai_spend WBR | D |
| R16-141 | PARK-RADAR kwartał | N |
| R16-142 | Hire human D3 | P |
| R16-143 | REJECT in-toto/GitFlow/… | R |

### 2.11 `INSTALL-UXCL.md`

| ID | Treść | St |
|---|---|---|
| R16-150 | 3 SKILL + PROC | D |
| R16-151 | Nie kopiuj OS/22–24 | R |
| R16-152 | Po INSTALL nie startuj L1 z INSTALL | D |

### 2.12–2.14 `JAK-PISZEMY*`

| ID | Treść | St |
|---|---|---|
| R16-160 | Surowiec; promocja L1–L3 | D |
| R16-161 | Leksem → GLOSSARY | D |
| R16-162 | Klasy komentarza | D |
| R16-163 | Diátaxis / jeden spec | D |
| R16-164 | Zakaz CODE/DOCS-OS | R |
| R16-170 | Podłoga żywa | D |
| R16-171 | L1–L3 patch | D |
| R16-172 | L4 glossary script | P |
| R16-173 | REJECT comments-skill / LLM-judge | R |
| R16-180 | Test = kod; izolacja PG | D |
| R16-181 | L5 MagicMock | P |
| R16-182 | Parse don’t validate | D |
| R16-183 | Debug naukowy | D |
| R16-184 | Hypothesis/mutmut HOLD | P |

### 2.15 `LEARNING-OS.md`

| ID | Treść | St |
|---|---|---|
| R16-190 | Pętla I UXCL vs II fabryka | A/N |
| R16-191 | learn_recurrence; karta krótka | N |
| R16-192 | SLA 7 dni; kubełki P-Y; retrieve 8–20 | D |
| R16-193 | Zakaz etat learning / auto-AGENTS | R |

### 2.16 `MECHANISMS.md`

| ID | Treść | St |
|---|---|---|
| R16-200 | Odrzut Culture Deck/OKR/DiRT | R |
| R16-201 | G0 PREMORT→PRR→LAUNCH | P |
| R16-202 | P-Y tygodniowo | N |
| R16-203 | Zero nowych skilli z mapy; E3 never | R |

### 2.17 `PROC-UXCL.md`

| ID | Treść | St |
|---|---|---|
| R16-210 | ux-continuous-loop.md | D |
| R16-211 | Pętla Signal→Closure | D |
| R16-212 | Tydzień P1–P8 | A |
| R16-213 | Privacy checklist | A |
| R16-214 | Meta-KPI Closure/PII | N |
| R16-215 | Busy → zero UXCL do OmniRoute | R |

### 2.18 `SH-CZYTAJ.md`

| ID | Treść | St |
|---|---|---|
| R16-220 | Kolejność czytania; zakaz w plaster | B |
| R16-221 | gate=success | D |
| R16-222 | Pakiety domknięte; ponowienie=D0 | B |

### 2.19 `SKILLS-OS.md`

| ID | Treść | St |
|---|---|---|
| R16-230 | 10+3 skilli paved road | D |
| R16-231 | skill_* pulse | N |
| R16-232 | Fire skill >4 tyg. | N |
| R16-233 | Zakaz 11. skill / COMMANDS-OS | R |

### 2.20 `ZRODLA-FABRYKA.md`

| ID | Treść | St |
|---|---|---|
| R16-240 | Bibliografia nie rytuał | B |
| R16-241 | Odrzut Culture/OKR/elite z n=4 | R |

### 2.21 Szablony / W38 (unikalne)

| ID | Treść | St |
|---|---|---|
| R16-250 | Actions permissions / brak PR_target+sekrety | D |
| R16-251 | L1–L3 commit procedura | D |
| R16-252 | PACK-STOP w ops + gate=success | D |
| R16-253 | IDLE-SESJA checklista | N |
| R16-254 | W38 ograniczenie | D |
| R16-255 | KNOWLEDGE-DRAFT → `_knowledge` | N |
| R16-256 | Pasmo unmeasured n=4 | N |
| R16-257 | Brak dependabot.yml = zamierzone | R |
| R16-258 | Po hire: required PR | P |
| R16-259 | Marketing B2C = D3 nie leftover | P |

**Licznik:** 20/20 plików + R16-001…272 (luki numeracji OK). Audyt 16b: twarde+false DONE+materialne → PLAN SH-R16-8…15.

---

## 3. Definicja „zrealizowane”

| Klasa | Znaczy |
|---|---|
| **DONE** | Jest w OmniRoute / GH Settings / egzekwowane haki |
| **NOW** | W kolejce `/noc` batch SH-R16-* albo docs tej promocji |
| **AFTER_527** | W PLAN jako leftover produktu; start gdy CURRENT dojdzie |
| **PARK** | W PLAN § Park + tu; warunek jawny; nie skip bez unparku |
| **REJECT** | Świadomy zakaz — zrealizowane jako „nigdy” |
| **BADANIA** | Konstytucja/inbox zostaje na `D:\`; treść **śledzona** tutaj; zero duplikatu kanonu bez potrzeby |

---

## 4. Audyt zamknięcia rejestru

Przed ogłoszeniem „Rejestr 16 IX zamknięty” (produktowo: po SH-R16-12…15 + UXCL-L1):

1. Szablony **29/29** w `docs/ops/szablony/`.
2. False DONE z audytu 16 IX = naprawione (SH-R16-8).
3. Materialne niezmapowane = w `fabryka-playbooki-sh.md` + wiersze SH-R16-12…15.
4. 20/20 plików w §0 = POKRYTE/DONE/BADANIA.
5. Push + CI `gate=success` na SHA docs.

Nie ogłaszaj elite. Nie zdejmuj pinu 2026-09-08c.

---

## 5. Domknięcie audytu 2026-09-16b (braki → PLAN `/noc`)

### 5.1 Twarde — DONE w tej promocji

| Brak audytu | Naprawa |
|---|---|
| 13 szablonów | skopiowane → 29/29 |
| PROC bez SIGNAL/EXPERIMENT/CLOSURE | ścieżki + status KANON |
| Brak KNOWLEDGE.md | w `ops/szablony/` |
| SH-R16-3 false DONE | status = pełne 29 |

### 5.2 False DONE — DONE w tej promocji

| Claim | Naprawa |
|---|---|
| PACK-STOP „D” bez pliku | `ops/szablony/PACK-STOP.md` |
| PROC BADANIA / extract „czeka” | kanon; D2 akceptuję; leftover UXCL-L1 |
| Context budget bez enumu | `context.mdc` + agentlint |
| SLA karty ≤7 dni | `friday-retrospective.md` |

### 5.3 Materialne — zmapowane do PLAN

| Treść | Gdzie |
|---|---|
| Playbooki P-A…P-Y, RACI, cooling 14d, CEO budget, Diátaxis | `ops/fabryka-playbooki-sh.md` (SH-R16-9) |
| Meta-KPI Closure ≤14d | PROC + SH-R16-11 |
| FACTORY-PULSE liczby | **SH-R16-12** czeka idle |
| Dependabot 1/tydzień | **SH-R16-13** czeka idle |
| Fire skill >4 tyg. | **SH-R16-14** czeka P-Y |
| PARK-RADAR kwartał | **SH-R16-15** czeka |
| UXCL-L1 / AI3 / Plat-HD / G0 / SBOM… | PLAN § Fala SH-R16 + §1.2–1.3 |

### 5.4 Nowe R16 (uzupełnienie luk)

| ID | Treść | St |
|---|---|---|
| R16-260 | Szablony 29/29 w OmniRoute | D |
| R16-261 | Enum context budget w AlwaysApply | D |
| R16-262 | SLA karty ≤7 dni w friday | D |
| R16-263 | Cooling 14 dni D3 | D (`fabryka-playbooki-sh`) |
| R16-264 | Budżet uwagi CEO | D |
| R16-265 | RACI skrót | D |
| R16-266 | Indeks P-A…P-Y | D |
| R16-267 | Diátaxis mapowanie docs | D |
| R16-268 | Meta-KPI Closure ≤14d | D (wiersz); egzekucja A |
| R16-269 | FACTORY-PULSE pierwsze liczby | N → SH-R16-12 |
| R16-270 | Dependabot 1 paczka/tydzień | N → SH-R16-13 |
| R16-271 | Fire skill >4 tyg. | N → SH-R16-14 |
| R16-272 | PARK-RADAR Q3/Q4 | N → SH-R16-15 |

**Kolejka `/noc` po tym commicie:** rytuały SH-R16-12…15 gdy idle; produkt **527.0**; potem UXCL-L1 / AI3 gdy CURRENT.

