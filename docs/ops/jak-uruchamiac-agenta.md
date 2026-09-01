# Jak odpalać `/plan-modul` i `/plaster` (widok Agenta)

Nie szukaj przycisku **„nowy czat”** — w oknie Agentów go nie ma.

Jesteś w **oknie Agentów** (nie w edytorze kodu). Windows.

## Gdzie co jest

| Potrzebujesz | Gdzie to jest |
|---|---|
| Nowa rozmowa | **Plus (`+`)** u góry okna Agentów (nad listą albo nad czatem). Albo: kliknij w **pole do pisania na dole**, potem `Ctrl+N` albo `Ctrl+R`. Albo: `Ctrl+Shift+P` → wpisz `New Agent` albo `New Chat` → Enter. |
| Lista starych rozmów | **Lewa kolumna** okna Agentów (historia). Kliknięcie wiersza wraca do starej rozmowy — do `/plaster` **nie** wracaj do wątku z Planu. |
| Tryb Plan vs Agent | W **polu wiadomości na dole**, zwykle **po lewej** nad klawiaturą / w pasku inputu: lista **Agent / Plan / Ask**. Szybko: kursor w polu, **`Shift+Tab`** aż zobaczysz **Plan** albo **Agent**. |
| Komenda `/plan-modul` | W tym samym polu na dole wpisz `/` — pojawi się lista komend projektu. Wybierz `plan-modul` albo dopisz ręcznie. |
| Komenda `/plaster` | Tak samo: `/` → `plaster`. |
| Komenda `/testy` | Tak samo: `/` → `testy`. **Po** akceptacji planu plików z `/plaster`, **zanim** powstanie kod. Tryb **Agent**. |

Otworzenie okna Agentów z edytora: `Ctrl+I`. Ty już jesteś w widoku Agenta — tego nie potrzebujesz.

## Kolejność jednej pozycji (np. 4.0 `port`)

1. **`+`** / `Ctrl+N` — pusta rozmowa. **`Shift+Tab`** → **Plan**. `/plan-modul`. Na końcu: `akceptuję`.
2. **`+`** / `Ctrl+N` — **druga** pusta rozmowa. **`Shift+Tab`** → **Agent**. `/plaster`. Agent wypisze plan plików i **czeka**. Ty: `akceptuję`.
3. **W tej samej** rozmowie Agent (nie wracaj do Planu): `/testy`. Agent pisze **czerwone** testy z delty i pokazuje, że padają. **Nie kod.**
4. Jak testy są czerwone: w **tej samej** rozmowie Agent napisz `implementuj` albo `kod`. Dopiero wtedy powstaje port / API / UI.
5. Na końcu agent zamyka plaster (`/zamknij`). CURRENT skacze dalej.

Po `/plan-modul` **nie** klikaj **Build** / **wdroż plan** w Cursorze.

`/testy` to nie opcjonalna rada. `/plaster` sam każe: po akceptacji planu plików osobna tura `/testy`, potem kod.

## Czego nie robić

- Nie dopisuj `/plaster` pod rozmową z `/plan-modul`.
- Nie szukaj menu „Nowy czat” jak w Messengerze.
- Nie pisz „zrób geografię” — wystarczy komenda; kolejka jest w `CURRENT.md`.
- Nie startuj 4.1 / 4.2 / Q2, dopóki bieżący plaster nie jest zamknięty i wypchnięty. Jeden naraz.

## Trzy plastry geografii (jeden po drugim)

Q1 to **nie** jeden wielki plaster. Kolejność z planu:

| Kiedy | Co | Ty robisz |
|---|---|---|
| **Teraz** | **4.0** `port` | Dokończ ten plaster: `/plaster` → `/testy` → `implementuj` → `/zamknij` (push). |
| Potem | **4.1** `location` + strefy | **Nowa** rozmowa. Najpierw Plan: `/plan-modul`. Potem nowa rozmowa Agent: `/plaster` → `/testy` → kod → `/zamknij`. |
| Potem | **4.2** `terminal` + WPI | Tak samo: Plan, potem plaster. |
| Potem | **Q2** kontrahenci | Dopiero po 4.2. |

Po `/zamknij` agent sam wpisuje do CURRENT **następny** numer. Ty nie wybierasz „który plaster” — czytasz CURRENT albo po prostu odpalasz `/plan-modul` albo `/plaster` zgodnie z **Etapem** w CURRENT.

Nie otwieraj trzech Agentów naraz. Nie dopisuj 4.1 w czacie 4.0.
