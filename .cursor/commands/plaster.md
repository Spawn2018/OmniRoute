---
description: Rozpoczyna realizację plastra według procedury
---

Przeczytaj `docs/state/CURRENT.md`.

Jeśli **Etap: Plan** albo brak zaakceptowanej delty dla tej pozycji kolejki:
**stop.** Nie pisz kodu. Powiedz: przełącz Cursor na tryb **Plan** i uruchom `/plan-modul`.
Kolejka: `docs/PLAN-REALIZACJA.md` § Kolejka realizacji.

Wykonaj w kolejności, zatrzymując się po każdym kroku po potwierdzenie:

1. Wypisz w jednym zdaniu, co budujesz i czego NIE budujesz.
2. Uruchom subagenta `lowca-duplikatow` z opisem funkcjonalności.
   Zaczekaj na werdykt ISTNIEJE / PODOBNE / BRAK.
3. Jeśli ISTNIEJE — zaproponuj rozszerzenie zamiast nowego kodu i przerwij.
4. Przeczytaj wyłącznie ten plik ze `docs/spec/`, który wskazuje CURRENT.md.
5. Sprawdź schemat bazy przez MCP Postgres. Nie czytaj modeli.
6. Napisz plan: pliki nowe, pliki zmieniane, kolejność, ryzyka.
   NIE PISZ KODU.

Zatrzymaj się i czekaj na akceptację planu.

Po akceptacji (osobna tura, nie ten sam przebieg): `/testy` — czerwone testy
z delty, bez implementacji. Dopiero potem kod.
