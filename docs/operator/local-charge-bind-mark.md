# Wiązanie dopłaty lokalnej (stance)

Na `/local-charge-bind-marks` zapisujesz **stance wiązania** charge/quote/other.

1. Wejdź na Wiązanie dopłaty lokalnej.
2. Wklej `mark_code` (snake 2–32) oraz `source_ref` (`fixture://local-charge-bind/…` albo `tenant:manual`).
3. Wybierz `bind_kind`: charge, quote albo other.
4. „Zapisz wiązanie dopłaty lokalnej” wstawia wiersz.

Czego tu nie ma: FK UUID do charge/quote, matching SQL, warning-jako-fakt, live HTTP.

Nazwy w kodzie: `local_charge_bind_mark` · `mark_code` · `bind_kind` · `source_ref` · `/local-charge-bind-marks`.
