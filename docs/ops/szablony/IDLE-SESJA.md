# IDLE-SESJA-YYYY-Www

Jedyna sesja firmy po `/noc` idle. Amazon WBR: **jedno** posiedzenie. DORA: **jedno** ograniczenie.  
Nie jest to piąty rytuał — to sklejka P-B (gdy czeka) + P-V + arkusze P-R/P-W/P-X + P-S.

**Stop:** `NOC-LIVE` = `busy` → tylko badania (notatki), zero promocji do repo.  
Gdy `idle`/`stop`: P-Y może liczyć w badaniach; INSTALL i nowy kanon w OmniRoute **tylko** po jawnym poleceniu.

Czas: agent ≤45 min (liczby). CEO ≤15 min (WBR §4). Łącznie **jedna** rozmowa, nie pięć.

## 0. Semafor

- [ ] `docs/state/NOC-LIVE.md` = idle / stop
- [ ] `git status` czysty na `origin/main` (albo WIP nie z tej sesji)
- [ ] Otwarte D2 ≤7

## 1. Instalacja UXCL — **DONE** (2026-09-16)

3 skille + PROC w OmniRoute. `skill_n` = 13. Nie powtarzaj INSTALL.  
Dziesięć skilli fabryki **nie ruszaj**.

## 2. Arkusze (załączniki, nie spotkania)

Wypełnij w tej samej turze; brak liczb = wpisz `unmeasured`, nie zmyślaj.

| Arkusz | Playbook | Źródło |
|---|---|---|
| `FACTORY-PULSE.md` | P-R | PROGRESS · post-plaster · `gh run list` |
| `CRAFT-PULSE.md` | P-W | post-plaster · `quality_floor` |
| `SKILLS-PULSE.md` | P-X | `.cursor/skills` (10 / 13) |
| `RECURRENCE.md` | P-V | PM-FAC/AAR z 28 dni |

Jedno ograniczenie na całą sesję (nie po jednym na arkusz).  
Opcjonalnie: wiersz `FINOPS-NOC.md` w WBR (faktura CEO). **Nie** wypełniaj `PARK-RADAR` tutaj — to kwartał.

## 3. Flush nauki (P-V) + kubełki (`friday-retrospective.md`)

To **ten sam dzień**, nie drugi rytuał „piątek operatora”. Źródło w repo: `docs/ops/friday-retrospective.md` (już żyje; nie edytuj w `/noc`).

Zamknięte PM-FAC/AAR bez karty → jedna karta `_knowledge` (commit **bez** agentlinta).  
Dwuobieg / higiena cytatu → **osobny** commit + `agentlint --write`.  
Opcjonalnie wiersz `docs-debt.md` — trzeci commit, nigdy w jednym z kartą albo AGENTS.

Prune AlwaysApply (≤3 / ~2k) **tylko** gdy jest co uciąć. Skill nietknięty >4 tyg. → Fire `23` §11, nie nowy skill.  
Cron D1 / issue „standup” = zakaz. Nie dump `22`–`24`.

## 4. WBR — jedyne wejście CEO

`szablony/WBR.md`. Wklej wyjątki z arkuszy, nie recenzuj ruffa. Max **1** prośba (albo „nic”).

## 5. Zakaz w tej sesji

Drugi `/noc`. Nowy `*-OS.md`. 11. skill. Unpark G0 bez PREMORT→PRR→LAUNCH. Claim elite. Sterowanie pod Minuty plastra. Pięć osobnych „pulse meetings”. Drugi „piątek” poza tą sesją. Mega-commit karta+debt+AGENTS. Rozbudowa pakietu zamiast wypełnienia tego WBR (`PACK-STOP.md` spada po tej sesji).
