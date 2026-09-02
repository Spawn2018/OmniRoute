# Piątkowa retrospektywa reguł / skills (Faza D)

**Cel:** prune context poisoning, nie „standup 30 osób”.  
**Automacja** może otworzyć issue `retro-YYYY-MM-DD`. **Nie** edytuje `AGENTS.md` / `GROUNDING.md` / `.cursor/rules`. Merge kontraktu robi człowiek. Agent wolno dać diff **w komentarzu issue**.

Ten plik jest **procedurą**, nie logiem. Log = zamknięte issues. Inaczej puchnie i sam truuje kontekst.

## Checklist (≤30 min)

1. AlwaysApply — czy nadal ≤3 i ≤~2k tokenów łącznie?
2. Skill nietknięty >4 tygodnie → archiwum albo skasuj.
3. `agentlint` baseline — czy ruszany świadomie, w tym samym commicie co treść?
4. Knowledge: karta po zdarzeniu, nie dump OSS. Max 8–20 retrieve.
5. Jedna decyzja ADR albo linia w PROGRESS — zero „omówimy”.
6. Czy leftover w `docs-debt.md` przestał być leftoverem?

## Trzy kubełki — osobne commity, nigdy razem

1. Karta `docs/_knowledge/` — bez agentlinta.
2. Wiersz w `docs-debt.md`.
3. Zmiana kontraktu — `python scripts/quality/agentlint.py --write` w **tym samym** commicie.

Sygnał do wyłączenia crona D1: issue zamykane bez czytania trzy tygodnie z rzędu.
