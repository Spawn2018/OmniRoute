# LAUNCH-G0 — tydzień pierwszego tenanta

Microsoft / Amazon launch review: **freeze ścieżki**, nie 205 UX.  
Po `PREMORT` + `PRR` z werdyktem `akceptuję unpark`.

- Klient (bez PII):
- STO: CEO
- Okno freeze (daty):

## Freeze (REQUIREMENT)

- [ ] Zero nowych BC / silników / live konektorów w oknie
- [ ] `/noc` tylko leftover *na critical path* albo stop nocy (D2)
- [ ] Job mierzony: extract-accept (nie `charge` jako event)
- [ ] Park live zostaje parkiem
- [ ] Sekrety wnosi człowiek; AI nie widzi
- [ ] Plat-HD: ticket → Twój OK; nie auto-fix

## Critical path (HHL)

RFQ → extract HITL → wycena/`charge` jako prawda → decyzja. Reszta = park.

## Rollback

Jedno zdanie jak gasisz host/IdP / Access:

## Werdykt

`freeze on` | `freeze off` | `abort launch`
