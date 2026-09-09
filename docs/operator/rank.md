# Oś rankingu

Na `/rank-marks` zapisujesz **znacznik osi rankingu zakupu** tenanta (cena, transit, wiarygodność, ślad, inne). To nie auto-award i nie paczka szkiców z Top N.

1. Wejdź na Oś rankingu. Wybierz oś (`price` / `transit` / `reliability` / `carbon` / `other`).
2. Podaj `source_ref` (`fixture://rank-mark/…` albo `tenant:manual`).
3. „Zapisz oś rankingu”.

Czego tu nie ma: ranking SQL, N szkiców maila, auto-award, suma w przeglądarce. Sieci i Top N zostają na `/networks`. Marża zostaje na `/charges`.

Nazwy w kodzie: `rank_mark` · `rank_kind` · `source_ref`.
