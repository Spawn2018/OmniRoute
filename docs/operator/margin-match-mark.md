# Dopasowanie podłogi (stance)

Na `/margin-match-marks` zapisujesz **stance wariancji** match/hold/waive/other.

1. Wejdź na Dopasowanie podłogi.
2. Wklej `mark_code` (snake 2–32) oraz `source_ref` (`fixture://margin-match/…` albo `tenant:manual`).
3. Wybierz `match_kind`.
4. „Zapisz dopasowanie podłogi” wstawia wiersz.

Czego tu nie ma: matching SQL lane, auto charge, FK do trip, live HTTP.

Nazwy w kodzie: `margin_match_mark` · `mark_code` · `match_kind` · `source_ref` · `/margin-match-marks`.
