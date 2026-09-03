# Zbiorcza faktura

Jedno zlecenie na fakturze to kotwica. Kolejne zlecenie tego **samego kontrahenta** dopisujesz osobno na `/invoices`.

1. Najpierw zapisz dwa zlecenia na `/shipments` (ten sam nabywca) i fakturę na pierwszym.
2. Wejdź na Faktury. Wklej `sales_invoice_id`, `shipment_id` dodatkowego zlecenia i `source_ref` (`fixture://collective-invoice/…` albo `tenant:manual`).
3. „Zapisz zbiorczą” wiąże to zlecenie z fakturą. System nie sumuje kwot i nie składa JPK.
4. Zlecenie, które już jest kotwicą faktury, odrzuca. Zlecenie innego kontrahenta też.

Czego tu nie ma: płatność wielu faktur jedną wpłatą, JPK, HTTP do ministerstwa. Sprzedaż zostaje na `/charges`. Faktura zostaje na `/invoices`.

Nazwy w kodzie: `collective_invoice` · `sales_invoice_id` · `shipment_id` · `source_ref`.
