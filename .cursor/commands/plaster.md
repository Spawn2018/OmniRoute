---
description: Rozpoczyna realizację plastra według procedury
---

Przeczytaj `docs/state/CURRENT.md`.

**Poza `/noc`:** `python scripts/quality/factory_cycle.py --start plaster`
Retrieve + podłoga + **delta produktu** w `docs/deltas/open/` (pliki `OS-*` się nie liczą).
Brak delty = stop. Pominięcie retrieve = plaster bez pamięci fabryki.
**W `/noc`:** nie powtarzaj `--start plaster` — preflight już zrobił `--start noc`.

**Wyjątek `/noc`:** nie zatrzymuj się po kroku 6 i nie czekaj na `akceptuję`. Od razu `/testy`, potem kod, **`/po-plastrze` (pełna tabela)**, `/zamknij` bez nowej rozmowy, commit + push, wróć do pętli. Szczegóły: `docs/ops/nocna-zmiana.md`. `/noc` nie pomija kartki jakości.

Jeśli **Etap: Plan** albo brak zaakceptowanej delty dla tej pozycji kolejki:
**stop.** Nie pisz kodu. Powiedz: przełącz Cursor na tryb **Plan** i uruchom `/plan-modul`.
Kolejka: `docs/PLAN-REALIZACJA.md` § Kolejka realizacji.
**Wyjątek `/noc`:** nie mów o trybie Plan — wykonaj `/plan-modul` w tym Agencie (opcja rekomendowana, push), potem wróć do plastra.

Jeśli **Etap: Refaktor**:
**stop.** Nie pisz plastra domenowego. Odpal `/refaktor`. F9.1 nie zgaduj. S1 nie startuj przy Q-E.

Jeśli zakres **powyżej trzech plików** (także hotfix / leftover **poza** kolejką Q) i nie ma jeszcze zaakceptowanego planu plików:
**stop.** Napisz plan (krok 6), czekaj. Nie koduj „bo to nie jest Q”.

Wykonaj w kolejności, zatrzymując się po każdym kroku po potwierdzenie:

1. Wypisz w jednym zdaniu, co budujesz i czego NIE budujesz.
2. Uruchom subagenta `lowca-duplikatow` z opisem funkcjonalności.
   Zaczekaj na werdykt ISTNIEJE / PODOBNE / BRAK.
3. Jeśli ISTNIEJE — zaproponuj rozszerzenie zamiast nowego kodu i przerwij.
4. Przeczytaj wyłącznie ten plik ze `docs/spec/`, który wskazuje CURRENT.md.
5. Sprawdź schemat w `backend/alembic/versions/` (najnowsza migracja tej tabeli) i w modelach **tego BC**. Nie czytaj wszystkich modeli.
6. Napisz plan: pliki nowe, pliki zmieniane, kolejność, ryzyka.
   NIE PISZ KODU.

Zatrzymaj się i czekaj na akceptację planu.

Po akceptacji (osobna tura, nie ten sam przebieg): `/testy` — czerwone testy
z delty, bez implementacji. Dopiero potem kod.

Po kodzie, **zanim** `/zamknij`: komenda `/po-plastrze`. Skopiuj tabelę 1:1 z `docs/ops/post-plaster.md` (wszystkie wiersze, zero skrótu). Max 3 poprawki; reszta → `docs/ops/docs-debt.md`. Push bez tej kartki = plaster niedomknięty.
