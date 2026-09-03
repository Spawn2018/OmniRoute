# Przepływ wyceny przy płatności

Lista nóg z opłaty (`buy` = wypływ, `sell` = wpływ) to jeszcze nie księga. Wiersz powstaje, gdy go **zapiszesz** na `/cashflows`.

1. Najpierw zapisz wycenę na `/quotations` i płatność na `/payments`.
2. Wejdź na Przepływy. Wklej `quotation_id`, `bank_payment_id` i `source_ref` (`fixture://cash-flow/…` albo `tenant:manual`).
3. „Zapisz przepływ” wiąże te dwa wiersze. System nie odejmuje wpływu od wypływu i nie kopiuje kwot.

Czego tu nie ma: kwota na tym wierszu, DSO, dopasowanie wyciągu. Sprzedaż zostaje na `/charges`. Płatność zostaje na `/payments`.

Nazwy w kodzie: `cash_flow` · `quotation_id` · `bank_payment_id` · `source_ref`.
