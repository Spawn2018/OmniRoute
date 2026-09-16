# L1–L3 — gotowy patch (nie stosuj przy `/noc`)

| Pole | Wartość |
|---|---|
| Wersja | **1.0 — 2026-09-16** |
| Status | BADANIA / SUROWIEC DO PROMOCJI. Nie `*-OS.md`. Nie next-ID. |
| Sens | Google: władza = *istniejący* style guide + linter, nie nowy etat. Dopisek klas komentarza **podnosi** `no-slop` bez skracania zakazów. |
| Warunek wpisu do OmniRoute | stop `/noc` + czysty git + jawne **„przenieś do kanonu”** + `python scripts/quality/agentlint.py --write` **w tym samym commicie** |
| Podłoga | lista ZAKAZANE w `no-slop` **bez skreśleń**. `quality_floor` nie w dół. |

Ten plik powstał, bo zgoda na zapis **gdy wnosi jakość**. Czwarty esej `JAK-PISZEMY-*` nie wnosi. Ten patch wnosi: mechanizm gotowy do jednego leftover.

---

## L1 — `.cursor/rules/no-slop.mdc`

**Zostaje w całości** blok ZAKAZANE (linie 6–16) i reszta WYMAGANE.

Po linii z przykładem NBP dopisz **dokładnie** (nie więcej):

```
- Klasy komentarza (gdy nazwa i typ nie niosą decyzji): prawo/urząd; invariant tenanta (RLS); odrzucona oczywistość (leftover w spec, nie w każdym wierszu); park CURRENT. Inaczej — brak komentarza.
```

Źródło: `JAK-PISZEMY.md` §3.1. Nie drugi plik AlwaysApply.

---

## L2 — `scripts/quality/craft_style.py`

**Zero nowej regex.** Już jest (`CONFIRMED` 2026-09-16): `Args:`, TODO, baner, `echo_comment_errors` (komentarz = nazwa `def`).  
Drugi detector „powtarza kod” = LLM-judge = odrzut.  
Przy promocji L1: tylko `agentlint.py --write`, nie nowa funkcja w OS-4.

---

## L3 — `docs/ops/post-plaster.md`

Wiersz **Dług / człowiek**, komórka Notatka — **zastąp** zdanie „Komentarz tylko *dlaczego*.” przez:

```
Komentarz tylko *dlaczego* (klasy: no-slop — prawo / invariant / odrzucona oczywistość / park).
```

Reszta wiersza (`just complexity` + `just dup` …) **bez zmian**. Nie nowy wiersz tabeli.

---

## Commit (gdy warunek)

Jeden leftover, nie 527.0:

1. L1 + L3 (L2 = brak diffu w `craft_style.py`).
2. `python scripts/quality/agentlint.py --write`
3. `just meta-gate` lokalnie.
4. Nie `--no-verify`. Nie drugi pisarz przy żywym `/noc`.

---

## Stop

- Stosowanie tego pliku z sesji firmy przy `/noc` busy.
- Nowy skill / hook / AlwaysApply.
- Skrót listy ZAKAZANE.
- L5 `MagicMock` (park — `JAK-PISZEMY-RESZTA.md`).
