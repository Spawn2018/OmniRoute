# Koszt obsługi przy procedurze

Lista SOP i wycen wybranego kontrahenta to jeszcze nie koszt obsługi. Wiersz powstaje, gdy go **zapiszesz** na `/cost-to-serve`.

1. Najpierw zapisz procedurę na `/customer-sops` i wycenę na `/quotations`.
2. Wejdź na Koszt obsługi klienta. Wklej `customer_sop_id`, `quotation_id` i `source_ref` (`fixture://cost-to-serve/…` albo `tenant:manual`).
3. „Zapisz koszt obsługi” wiąże te dwa wiersze. System nie sumuje wycen i nie liczy stawki godziny.

Czego tu nie ma: kwota na tym wierszu, ABC, stawka godziny. Sprzedaż zostaje na `/charges`. Procedura zostaje na `/customer-sops`.

Nazwy w kodzie: `cost_to_serve` · `customer_sop_id` · `quotation_id` · `source_ref`.
