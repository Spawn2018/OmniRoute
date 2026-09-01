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
| Komenda `/testy` | Tak samo: `/` → `testy`. **Po** akceptacji planu plików z `/plaster`, **zanim** powstanie kod. Tryb **Agent**. W `/noc` agent nie czeka na to słowo. |
| Komenda `/noc` | `/` → `noc`. Godzina obowiązkowa: `/noc 7` = pętla do 7:00. Umowa: [nocna-zmiana.md](nocna-zmiana.md). |

Otworzenie okna Agentów z edytora: `Ctrl+I`. Ty już jesteś w widoku Agenta — tego nie potrzebujesz.

## Kolejność jednej pozycji (np. 4.0 `port`)

1. **`+`** / `Ctrl+N` — pusta rozmowa. **`Shift+Tab`** → **Plan**. `/plan-modul`. Na końcu: `akceptuję`.
2. **`+`** / `Ctrl+N` — **druga** pusta rozmowa. **`Shift+Tab`** → **Agent**. `/plaster`. Agent wypisze plan plików i **czeka**. Ty: `akceptuję`.
3. **W tej samej** rozmowie Agent (nie wracaj do Planu): `/testy`. Agent pisze **czerwone** testy z delty i pokazuje, że padają. **Nie kod.**
4. Jak testy są czerwone: w **tej samej** rozmowie Agent napisz `implementuj` albo `kod`. Dopiero wtedy powstaje port / API / UI.
5. Na końcu agent zamyka plaster (`/zamknij`). CURRENT skacze dalej.

Po `/plan-modul` **nie** klikaj **Build** / **wdroż plan** w Cursorze.

`/testy` to nie opcjonalna rada. `/plaster` sam każe: po akceptacji planu plików osobna tura `/testy`, potem kod.

## Push: bramka włącza się sama

Jednorazowo, raz na komputer (wklej agentowi albo wpisz w PowerShellu w katalogu repo):

```
powershell -ExecutionPolicy Bypass -File scripts/install-hooks.ps1
```

Od tej chwili każdy `git push` z tego komputera najpierw odpala pełną bramkę
(`just gate` — to samo, co GitHub Actions). Trwa **ok. 70 sekund**. Jeśli coś pada,
push **nie idzie** i w oknie widzisz, co naprawić. To jest dobra wiadomość: czerwony
GitHub kosztuje więcej niż te 70 sekund.

Bramka **nie** sprawdza migracji bazy, `pip-audit` ani testów integracyjnych —
te wymagają uruchomionego Postgresa i OpenFGA. Robi to CI po pushu.

Najczęstsza porażka to `agentlint`: ktoś zmienił `AGENTS.md` albo reguły w `.cursor/rules/`
i nie przepisał odcisku. Hook wypisze wtedy gotowe polecenie do wklejenia — nie trzeba
nic wymyślać. Samo to sprawdzenie trwa sekundę: `just meta-gate`.

Sprawdzenie, czy jest włączona: `git config --get core.hooksPath` ma wypisać `scripts/githooks`.

### Furtka awaryjna

`git push --no-verify` przepycha z pominięciem bramki. To **wyjątek**, nie sposób pracy:
używa się go, gdy trzeba wypchnąć samą poprawkę do dokumentacji przy zepsutym
lokalnym środowisku. Po użyciu CI i tak sprawdzi wszystko — jeśli GitHub zaświeci
na czerwono, naprawa wraca do ciebie.

## Czego nie robić

- Nie dopisuj `/plaster` pod rozmową z `/plan-modul`.
- Nie szukaj menu „Nowy czat” jak w Messengerze.
- Nie pisz „zrób geografię” — wystarczy komenda; kolejka jest w `CURRENT.md`.
- Nie startuj kolejnej pozycji Q, dopóki bieżący plaster nie jest zamknięty i wypchnięty — chyba że to pętla `/noc` (jeden cykl naraz, potem następny z CURRENT).

## Noc (`/noc 7`)

Szczegóły: [nocna-zmiana.md](nocna-zmiana.md).

1. Tryb **Agent**. Komputer nie usypia. Żaden inny agent nie pisze. `git status` czysty.
2. Wpisz **`/noc 7`** (albo inną godzinę rano). Agent sam odpala `scripts/noc-preflight.ps1` (Postgres, OpenFGA, internet, GitHub). FAIL = stop.
3. Do tej godziny: plan + push, plaster + push, kolejna pozycja z CURRENT. Nie klikasz `akceptuję`.
4. Po godzinie: raport w czacie (co weszło, gdzie jesteśmy, ile w kolejce, problemy, pochwały).

W dzień nadal: `+` / `Ctrl+N`, tryb Plan do `/plan-modul`, druga rozmowa Agent do `/plaster`. Postgres: `pg_ctl -D tools\pgdata -o "-p 5432" start`.

## Kolejka

Nie zapamiętuj numeru plastra. Po `/zamknij` (albo cyklu `/noc`) tablica jest w `CURRENT.md`. Dziennie: `/plan-modul` albo `/plaster` zgodnie z **Etapem**. Nocą: jedna rozmowa, pętla aż do godziny.

Nie otwieraj trzech Agentów naraz na ten sam folder.
