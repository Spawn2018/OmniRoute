# Wariancja przejazdu (stance)

Na `/trip-variance-marks` zapisujesz **stance wariancji** expected/actual/gap/other.

1. Wejdź na Wariancje przejazdu.
2. Wklej `mark_code` (snake 2–32) oraz `source_ref` (`fixture://trip-variance/…` albo `tenant:manual`).
3. Wybierz `variance_kind`.
4. „Zapisz wariancję przejazdu” wstawia wiersz.

Czego tu nie ma: SQL na charge, druga marża, FK do trip, live HTTP.

Nazwy w kodzie: `trip_variance_mark` · `mark_code` · `variance_kind` · `source_ref` · `/trip-variance-marks`.
