# Tygodniowy refaktor (Faza D)

Skill: `.cursor/skills/refaktor-pass/SKILL.md`

Po **każdym** plasterze: `docs/ops/post-plaster.md` (pełna tabela, max 3 poprawki).
Ten plik = slot tygodniowy na ruchy **poza** plasterem i **poza** diffem. Nie łącz z domeną. Nie fałszuj `refactor_ratio` w plasterze.

## Rytm

1. Slot 60–90 min / tydzień (nie łącz z plastrami domenowymi).
2. `just complexity` · `just dup` · `python scripts/quality/refactor_ratio.py`
3. Max 3 zmiany behawioralnie neutralne; po każdej `just test-unit`.
4. Cel: ratio przeniesione/dodane ≥ 10% w oknie tygodnia.

## Issue template (opcjonalnie)

Tytuł: `refactor-week-YYYY-WW`  
Body: wynik `just dup` + 3 kandydaty.
