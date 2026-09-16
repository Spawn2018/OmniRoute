# PRR-G0 — Production Readiness (Google SRE / Amazon ORR — skrót)

Trigger: **nowy klient**, zanim D2 unpark host/IdP. Nie na plaster HITL.  
Kolejność: `PREMORT.md` → **ten plik** → `LAUNCH.md` → D2.  
Każde NIE / leftover bez ownera = **nie unpark**.

Kotwica: SRE book (PRR); publiczne ORR/launch reviews. Nie DiRT. Nie chaos.

## 0. Zakres

- Tenant / klient (bez PII w tej karcie):
- Host + domena (VISION E.3 — jeśli puste = D2/D3, nie zgaduj w nocy):
- IdP (S53 / Auth0) — tylko gdy CURRENT wskaże:

## 1. Izolacja i sekrety

- [ ] RLS + test izolacji na tabelach, których klient użyje
- [ ] Zero SQL cross-tenant w ścieżce TSL
- [ ] Sekrety tenanta: szyfrowane, AI nie widzi, nie w logu/promptcie
- [ ] Threat model: `docs/ops/threat-model-tenant-hitl.md` przeczytany pod ten launch
- [ ] OpenFGA: deny-default na endpointach ścieżki

## 2. HITL i model

- [ ] Extract: brak zapisu L0–2 z modelu
- [ ] Accept extractu = człowiek
- [ ] Job #1 nazwany (extract-accept) — eventy tylko po L0
- [ ] Żywy OpenAI w CI = nadal Park

## 3. Prawda pieniądza

- [ ] `charge` = jedyna marża; Decimal
- [ ] Echo k6 **nie** jest claimem DoD wobec klienta

## 4. Operacja (ludzie, nie Temporal)

- [ ] STO (single-threaded owner) launch = CEO
- [ ] SEV: kto wstaje przy SEV-1 (`szablony/SEV.md`) — dziś: CEO + stop drugiego pisarza
- [ ] Andon: `--no-verify` zakazany na hoście
- [ ] Backup/restore hosta: jest / leftover / D2 (nie wymyślaj vendor)

## 5. Observability i budżet

- [ ] Factory pulse znany albo jawne `unmeasured` (nie „elite”)
- [ ] Tenant SLO: N/A albo liczby — bez liczb nie claim p95
- [ ] Bundle JS: `just perf` real (< 250 kB) — to gate, nie marketing

## 6. Rollback

- [ ] Jak wracasz host/IdP (DNS / Access / feature freeze), jedno zdanie:
- [ ] Park live konektorów zostaje parkiem

## 7. Łańcuch, dostępność, CRA (`GIGANT-LUKI-2026.md`)

- [ ] Ruleset `main`: force-push/delete zablokowane (`GITHUB-MAIN.md`)
- [ ] Dependabot alerts ON; auto-PR OFF przy busy nocy
- [ ] Backup/restore hosta (już §4) + SBOM/attestation **jeśli** jest obraz
- [ ] EAA: poza zakresem **albo** WCAG 2.2 AA na ścieżce operatora (prawnik / leftover)
- [ ] CRA: nie manufacturer **albo** ścieżka 24/72 h + SRP (prawnik; `EAA-CRA.md`)
- [ ] `factory_ai_spend` znany albo `unmeasured` — nie claim SLO $

## Werdykt CEO

`czeka` | `akceptuję unpark` | `park` | `odrzucam`

Data:
