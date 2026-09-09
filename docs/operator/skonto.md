# Skonto

Na `/cash-discounts` zapisujesz **rodzaj skonta** przy istniejącej fakturze sprzedaży (np. `skonto`, `reserve`). To nie kwota na wierszu i nie wyciąg CAMT.

1. Wejdź na Skonto. Wklej `sales_invoice_id` faktury tenanta.
2. Wpisz kind snake (2–32 znaki).
3. „Zapisz skonto” z `source_ref` (`fixture://cash-discount/…` albo `tenant:manual`).

Czego tu nie ma: Decimal skonta, noty korygujące, period lock, ingest CAMT, biała lista przy przelewie, suma w przeglądarce. Marża zostaje na `/charges`. Faktura zostaje na `/invoices`. Płatność zostaje na `/payments`.

Nazwy w kodzie: `cash_discount` · `sales_invoice_id` · `discount_kind` · `source_ref`.
