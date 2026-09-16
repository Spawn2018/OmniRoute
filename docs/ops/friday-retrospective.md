# Piątkowa retrospektywa reguł / skills (Faza D)

**Cel:** prune context poisoning, nie „standup 30 osób”.  
Operator **nie** prowadzi tego rytmu. C2 (`check_agent_refs`) i `craft_close` jadą w `just meta-gate` przy każdym `/zamknij`. Cron D1 zostaje wyłączony — issue, którego nikt nie czyta, nic nie uczy.

**Nie** edytuje `AGENTS.md` / `GROUNDING.md` / `.cursor/rules` automatycznie. GROUNDING tylko człowiek + ADR. Higiena cytatu (martwy `just` / MCP) = osobny commit + `agentlint.py --write`, bez nowych zasad.

Ten plik jest **procedurą na wypadek ręcznego prune**, nie logiem i nie checklistą piątku operatora.

## Checklist (≤30 min)

1. AlwaysApply — czy nadal ≤3 i ≤~2k tokenów łącznie?
2. Skill nietknięty >4 tygodnie → archiwum albo skasuj.
3. `agentlint` baseline — czy ruszany świadomie, w tym samym commicie co treść?
4. Knowledge: karta po zdarzeniu, nie dump OSS. Max 8–20 retrieve. **SLA:** karta ≤**7 dni** od close plastra / PM-FAC (LEARNING-OS); zaległa = kubełek debt albo dwuobieg, nie druga karta.
5. Jedna decyzja ADR albo linia w PROGRESS — zero „omówimy”.
6. Czy leftover w `docs-debt.md` przestał być leftoverem?

## Trzy kubełki — osobne commity, nigdy razem

1. Karta `docs/_knowledge/` — bez agentlinta.
2. Wiersz w `docs-debt.md`.
3. Zmiana kontraktu — `python scripts/quality/agentlint.py --write` w **tym samym** commicie.

D1 nie włączamy. Ta checklista jest na ręczny prune, nie na piątek operatora.
