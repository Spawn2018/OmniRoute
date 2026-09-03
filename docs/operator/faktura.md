# Faktura sprzedaży

Kwota sprzedaży z opłaty to jeszcze nie faktura. Wiersz powstaje, gdy go **zapiszesz** na `/invoices`, na konkretnym zleceniu.

1. Najpierw zapisz zlecenie na `/shipments`.
2. Wejdź na Faktury. Wklej `shipment_id`, rodzaj (`issued`, `noted` albo `other`), numer dokumentu (`invoice_ref`) i `source_ref` (`fixture://sales-invoice/…` albo `tenant:manual`).
3. „Zapisz fakturę” wstawia wiersz. System nie wysyła nic do ministerstwa i nie kopiuje marży.
4. Gdy masz już numer sesji, wklej `invoice_id` i `ksef_ref` (`fixture://ksef/…` albo `ksef://…`) i kliknij „Zapisz numer sesji”. To tylko notatka na tym samym wierszu.

Czego tu nie ma: połączenie z bramką ministerstwa, XML, licznik numeru, kwota na tym wierszu, auto-wiersz z `charge`. Sprzedaż zostaje na `/charges` i `/finance`.

Nazwy w kodzie: `sales_invoice` · `invoice_kind` · `invoice_ref` · `source_ref` · `ksef_ref`.
