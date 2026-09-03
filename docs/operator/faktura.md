# Faktura sprzedaży

Kwota sprzedaży z opłaty to jeszcze nie faktura. Wiersz powstaje, gdy go **zapiszesz** na `/invoices`, na konkretnym zleceniu.

1. Najpierw zapisz zlecenie na `/shipments`.
2. Wejdź na Faktury. Wklej `shipment_id`, rodzaj (`issued`, `noted` albo `other`), numer dokumentu (`invoice_ref`) i `source_ref` (`fixture://sales-invoice/…` albo `tenant:manual`).
3. „Zapisz fakturę” wstawia wiersz. System nie wysyła nic do KSeF i nie kopiuje marży.

Czego tu nie ma: KSeF, XML, licznik numeru, kwota na tym wierszu, auto-wiersz z `charge`. Sprzedaż zostaje na `/charges` i `/finance`.

Nazwy w kodzie: `sales_invoice` · `invoice_kind` · `invoice_ref` · `source_ref`.
