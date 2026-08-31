---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2027-02-28
---

# Strategia gałęzi i wydań

Praca jednoosobowa — model prosty, ale z zachowaniem dyscypliny,
która ma sens także po ewentualnym dołączeniu drugiej osoby.

## Gałęzie

```
main                zawsze wdrażalna, chroniona
plaster/<id>        jedna gałąź na plaster, drzewo robocze
hotfix/<opis>       poprawka krytyczna z produkcji
```

**Drzewa robocze zamiast przełączania gałęzi:**

```bash
git worktree add ../work-2.4 -b plaster/2.4
```

Gałąź główna zostaje zielona, porzucenie nieudanego plastra to usunięcie
katalogu.

## Cykl plastra

```
delta-spec → gałąź → commity robocze → rebase → PR → bramka → merge
```

Commity robocze z `--no-verify` co 30–40 minut. Przed PR `git rebase -i`
i sprzątanie historii do jednego commita z opisem.

## Ochrona gałęzi głównej

```
□ PR wymagany, bez wypychania bezpośrednio
□ bramka CI musi przejść
□ automatyczny przegląd (BugBot, pr-agent) bez blokujących uwag
□ liniowa historia, bez merge commitów
```

## Wersjonowanie

Semantyczne, generowane przez `release-please` z konwencjonalnych commitów.

| Zmiana | Człon |
|---|---|
| Zmiana łamiąca API publiczne | major |
| Nowa funkcja | minor |
| Poprawka | patch |

**Po pierwszej integracji klienta wersja API nie może się zepsuć.**
Polityka deprecacji: dwanaście miesięcy uprzedzenia, wersje równoległe.

## Wydania

Wdrożenie z gałęzi głównej po przejściu bramki. Bez okien wydawniczych —
wdrażamy, gdy gotowe. Wyjątek: migracje wymagające okna serwisowego,
komunikowane klientom z siedmiodniowym wyprzedzeniem.
