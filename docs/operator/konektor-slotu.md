# Konektor slotu

Na `/terminal-slot-connectors` dopisujesz **capability slotu** terminalu: kod konektora, kod terminalu jako dana (nie FK do katalogu ISPS), tryb `api` / `email_hitl` / `portal_task` / `unsupported` oraz godziny otwarcia, zamknięcia i odcięcia (N4). To nie jest awizacja doku i nie jest rezerwacja okna.

1. Wejdź na Konektor slotu. Wpisz kod konektora i kod terminalu (snake 2–32).
2. Wybierz tryb z listy. `api` znaczy „ten terminal ma kontrakt API” — nie wywołuje Navis N4.
3. Podaj godziny lokalne bramy i odcięcie. Nocna zmiana (22:00–06:00) jest legalna; system nie obiecuje slotu.
4. Podaj `source_ref` (`fixture://terminal-slot-connector/…` albo `tenant:manual`).
5. „Zapisz konektor slotu”. Ten sam kod, ten sam terminal albo to samo `source_ref` u tenanta nie wejdzie drugi raz.

Czego tu nie ma: live HTTP, Selenium, checkbox potwierdzenia, `dock_appointment`, yard, optymalizator, gwarancja prawna. Marża zostaje na `/charges`. Awizacja magazynu zostaje na `/dock-appointments`.

Nazwy w kodzie: `terminal_slot_connector` · `connector_code` · `terminal_code` · `mode` · `opens_local` · `closes_local` · `cutoff_local` · `source_ref`.
