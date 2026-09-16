---
name: ux-privacy-instrument
description: L0→L1 UXCL — checklista privacy i nazwy eventów jobowych bez PII. Nie plaster produktu bez CURRENT.
---

# ux-privacy-instrument

Jeden job: **wolno mierzyć** i **jak nazwać event**, zanim ktokolwiek doda PostHog.

## Wejście (obowiązkowe)

1. `docs/state/CURRENT.md`
2. Lokalne `docs/state/NOC-LIVE.md` — jeśli `busy` / trwa `/noc`: **zero edycji** `frontend/` i `docs/ops` w OmniRoute. Wolno karta w `D:\OMNIROUTE-badania`.
3. Job: **extract-accept**, dopóki inbox D2 nie wskaże inaczej. Nie drugi job (`charge`) w tym samym cyklu.
4. `docs/ops/ux-continuous-loop.md` § P2. Nie wczytuj `22`/`23`/`24` w sesji plastra.

## Kroki

1. Purpose: jedno zdanie po co event (job completion / drop / czas). Brak celu = stop.
2. Checklist z PROC-UXCL P2 — wypisz TAK/NIE. Jedno NIE = stop instrumentacji.
3. Zaproponuj **nazwy** eventów i properties z GLOSSARY. Każde property: skąd wartość, czy może być PII.
4. Replay: wyłączony albo osobna zgoda. Nie mieszaj z eventami.
5. Jeśli zmiana kodu: `lowca-duplikatow`. >3 pliki → plan, czekaj D2 (wyjątek tylko `/noc` na CURRENT — ten skill **nie** jedzie w `/noc` jako next-ID).
6. Test: fixture eventu **nie** zawiera NIP, e-mail, sekretu, treści maila, `input_text` extractu.
7. Wyjście: karta „L0 OK / NIE” + lista eventów. Nie dashboard. Nie A/B.

## DoD

- Checklist kompletna.
- Jeden job (extract-accept), nie vanity pageview jako primary.
- Zero scoringu osoby.

## Zakaz

- FullStory / heatmap / session replay bez hipotezy + DPIA
- Sekrety w eventach, promptach, logach
- Vanity DAU jako metryka sukcesu
- Live HTTP / nowe konektory
- Auto-L3, zapis extractu, mutacja `charge`
- Drugi pisarz na `main` przy `/noc` busy
- Traktowanie `ab_sus_mark` jako włączonego A/B
