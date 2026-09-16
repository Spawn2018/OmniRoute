# PM-FAC-YYYYMMDD

Amazon Correction of Error (publiczny wzorzec) + SRE blameless.  
Trigger: `24` §2 A2. Kopiuj do `postmortems/` **dopiero przy zdarzeniu**. WIP: max 1 otwarty.

- SEV (`szablony/SEV.md`): 1 | 2
- Trigger: ≥2 CI czerwone na Q | nocka martwa | push bez bench | dwaj pisarze | CURRENT ≠ git | `--no-verify` | PROGRESS PRZESZLO przy `gate` ≠ success (`cancelled` też)

## Fakt

- Co się wydarzyło (nie wina etatu):
- Timeline (preflight → … → stop):
- Impact: git / CURRENT / klient (po G0):

## 5 Whys (CoE)

1. Dlaczego się wydarzyło?
2. Dlaczego to było możliwe?
3. Dlaczego mechanizm nie zatrzymał?
4. Dlaczego nie wykryto wcześniej?
5. Jaka zmiana mechanizmu (nie „agent uważniejszy”)?

Przyczyna bezpośrednia / warunki:

Co zadziałało (Andon, hak):

## Akcje (max 3)

1. owner (etat|D2) · termin:
2.
3.

- Luka detekcji (czemu Andon spóźnił / nie było):
- Zmiana kontraktu? nie | tak → inbox + `agentlint` przy instalacji
- Status: open | closed
- Po closed: `szablony/KNOWLEDGE.md` w **tej sesji** (strop WBR). Flush `_knowledge` = P-V po idle. Recurrence: `LEARNING-OS.md`.
