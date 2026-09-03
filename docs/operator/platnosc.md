# Płatność faktury na rachunek

IBAN kontrahenta i sprzedaż z opłaty to jeszcze nie płatność. Wiersz powstaje, gdy go **zapiszesz** na `/payments`.

1. Najpierw zapisz fakturę na `/invoices` i rachunek na `/parties`.
2. Wejdź na Bank i płatności. Wklej `sales_invoice_id`, `party_bank_account_id` i `source_ref` (`fixture://bank-payment/…` albo `tenant:manual`).
3. „Zapisz płatność” wiąże te dwa wiersze. System nie odejmuje kwot i nie wysyła SEPA.

Czego tu nie ma: kwota na tym wierszu, wyciąg, live bank, zapis IBAN z tego ekranu. Sprzedaż zostaje na `/charges`. Rachunek zostaje na `/parties`.

Nazwy w kodzie: `bank_payment` · `sales_invoice_id` · `party_bank_account_id` · `source_ref`.
