# ANDON-YYYYMMDD

Wypełnij przy czerwonym gate/CI. Toyota / lean: **stop linii**, nie `--no-verify`.

- Q / plaster (z CURRENT, nie zgaduj):
- Pierwszy czerwony (fakt):
- Naprawa w tym samym Q? tak / nie
- Ile faili z rzędu na tym Q: 1 | 2 | **3+**
- Hak ominięty? nie | tak → trigger A2 (PM-FAC)

## Reguła

- 1–2 fail: naprawa = plasterownik, ten sam Q.
- 3× fail: karta + leftover `docs-debt` + D1 (raport). **Nie** nowy skill.
- Trigger A2 (`24` §2): PM-FAC, nie sam ten Andon.
- To jest `factory_recover` (`DORA-FABRYKA.md`). Wpisz wynik do następnego FACTORY-PULSE (sesja firmy, nie noc).
- STUB jako PRZESZŁO / skrót post-plaster / spadła podłoga / critic commit → też Andon (`CRAFT-OS.md`). Nie zatrudniaj recenzenta.
- Nowy SKILL.md poza hire/INSTALL albo `skill_n` ≠ 10/13 → Andon (`SKILLS-OS.md`). Nie pisz bliźniaka.
- Nadaj SEV (`szablony/SEV.md`). SEV-1 → PM-FAC.

Zakaz: drugi `/noc`, Cloud Agent na `main`, force-push.
