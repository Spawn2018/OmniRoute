# Koszt pieniądza przy płatności

Kurs NBP i kupno z opłaty to jeszcze nie koszt pieniądza. Wiersz powstaje, gdy go **zapiszesz** na `/money-cost`.

1. Najpierw zapisz płatność na `/payments` i kurs na `/nbp-rates`.
2. Wejdź na Koszt pieniądza. Wklej `bank_payment_id`, `nbp_rate_id` i `source_ref` (`fixture://money-cost/…` albo `tenant:manual`).
3. „Zapisz koszt” wiąże te dwa wiersze. System nie mnoży kwot kursem i nie liczy odsetek.

Czego tu nie ma: kwota na tym wierszu, WACC, dni finansowania, zapis kursu z tego ekranu. Sprzedaż i kupno zostają na `/charges`. Kurs zostaje na `/nbp-rates`.

Nazwy w kodzie: `money_cost` · `bank_payment_id` · `nbp_rate_id` · `source_ref`.
