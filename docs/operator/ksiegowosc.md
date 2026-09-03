# Dekret opłaty na fakturę

Join kodu opłaty z nazwą katalogu to jeszcze nie księgowość. Wiersz powstaje, gdy go **zapiszesz** na `/bookkeeping`.

1. Najpierw zapisz opłatę na `/charges` i fakturę na `/invoices`.
2. Wejdź na Księgowość. Wklej `charge_id`, `sales_invoice_id` i `source_ref` (`fixture://bookkeeping/…` albo `tenant:manual`).
3. „Zapisz dekret” wiąże te dwa wiersze. System nie odejmuje sprzedaży od kupna i nie składa JPK.

Czego tu nie ma: kwota na tym wierszu, JPK, HTTP do ERP. Sprzedaż zostaje na `/charges`. Faktura zostaje na `/invoices`.

Nazwy w kodzie: `bookkeeping` · `charge_id` · `sales_invoice_id` · `source_ref`.
