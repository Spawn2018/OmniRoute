# Dopasowanie dopłaty lokalnej (stance)

Na `/local-charge-match-marks` zapisujesz **stance wariancji** match/hold/waive/other.

1. Wejdź na Dopasowanie dopłaty lokalnej.
2. Wklej `mark_code` (snake 2–32) oraz `source_ref` (`fixture://local-charge-match/…` albo `tenant:manual`).
3. Wybierz `match_kind`.
4. „Zapisz dopasowanie dopłaty lokalnej” wstawia wiersz.

Czego tu nie ma: matching SQL vs local_charge, warning-jako-fakt, FK do local_charge, live HTTP.

Nazwy w kodzie: `local_charge_match_mark` · `mark_code` · `match_kind` · `source_ref` · `/local-charge-match-marks`.
