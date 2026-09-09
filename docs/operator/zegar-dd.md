# Zegar DD

Na `/free-time-clocks` zapisujesz **zegar demurrage/detention/rollover** tenanta (rodzaj i dni wolne). To nie odliczanie od wjazdu na terminal i nie szkic opłaty.

1. Wejdź na Zegar DD. Wybierz rodzaj (`demurrage` / `detention` / `mixed` / `rollover`) i wpisz liczbę dni wolnych (całkowita, ≥ 0).
2. Podaj `source_ref` (`fixture://free-time-clock/…` albo `tenant:manual`).
3. „Zapisz zegar D&D”.

Czego tu nie ma: countdown, remaining days, blank sailing, kolumny na kontenerze, live HTTP armatora, myto, suma w przeglądarce. Kontener ISO zostaje na `/shipments`. Marża zostaje na `/charges`.

Nazwy w kodzie: `free_time_clock` · `clock_kind` · `free_days` · `source_ref`.
