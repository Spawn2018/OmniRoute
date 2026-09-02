---
description: Etap Plan dla pozycji kolejki — rozmowa i delta, zero kodu produktu
---

Przeczytaj `docs/state/CURRENT.md` i `docs/PLAN-REALIZACJA.md` § Kolejka realizacji.

**Wyjątek `/noc`:** zostań w Agencie. Nie przełączaj na tryb Plan. Nie czekaj na `akceptuję`. Opcja rekomendowana, delta, `just docs`, commit + push, od razu `/plaster` jeśli przed godziną stopu. Szczegóły: `docs/ops/nocna-zmiana.md`.

Jeśli w Cursorze jesteś w trybie Agent **i to nie jest `/noc`**: przełącz na **Plan** (ten sam wybór co Agent / Multitask). Nie implementuj.

Ta komenda = wydmuszka albo kolejna pozycja Q. Nie dumpuj `Informacje z claude/`. Nie twórz 70 stubów.

Wykonaj i zatrzymaj się po planie (czekaj na akceptację człowieka):

1. Wypisz pozycję kolejki z CURRENT (np. Q-E1, S1 M-32) oraz czego NIE robisz. Parked z PLAN (M-02, Auth0, portale) **pomijaj**, chyba że CURRENT to właśnie ten ID. Kolizje ID z PLAN § mapa kolizji — nie nadpisuj żywego M-07/M-08/M-52/M-57.
2. Jeśli archiwum jest potrzebne: **tylko** nagłówek i obiekty tego jednego M-xx — nie ładuj aneksów.
3. Ustal z człowiekiem: job operatora (ekran w tym samym plasterze), tabele, poza zakresem, OpenFGA, RLS.
4. Nadaj **żywy** kod modułu, gdy archiwum koliduje z M-07/M-08 już w kodzie.
5. Utwórz lub uzupełnij `docs/deltas/open/<id>.md` (`/delta`). Puste = „DO USTALENIA”, pytania na końcu.
6. Zaktualizuj `CURRENT.md`: Etap **Plan** → po akceptacji człowieka dopiero wolno `/plaster`.
7. NIE PISZ kodu backendu, migracji ani UI.

Po akceptacji: człowiek otwiera **nową** rozmowę w trybie Agent i `/plaster`.
