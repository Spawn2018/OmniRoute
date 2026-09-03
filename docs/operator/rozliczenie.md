# Rozliczenie wyceny z fakturą

Para wycena + `sell` z opłaty to jeszcze nie rozliczenie. Wiersz powstaje, gdy go **zapiszesz** na `/quote-invoices`.

1. Najpierw zapisz wycenę na `/quotations` i fakturę na `/invoices`.
2. Wejdź na Rozliczenie wyceny. Wklej `quotation_id`, `sales_invoice_id` i `source_ref` (`fixture://quote-invoice-settlement/…` albo `tenant:manual`).
3. „Zapisz rozliczenie” wiąże te dwa wiersze. System nie odejmuje kwot i nie kopiuje marży.

Czego tu nie ma: kwota na tym wierszu, automatyczne dopasowanie po `rate_line_id`, wymóg że faktura siedzi na zleceniu z tą samą wyceną. Sprzedaż zostaje na `/charges`.

Nazwy w kodzie: `quote_invoice_settlement` · `quotation_id` · `sales_invoice_id` · `source_ref`.
