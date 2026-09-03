# Tablica finansowa

Marża, kurs NBP i limit kontrahenta to fakty z katalogów. Faktura sprzedaży to osobny wiersz — tablica go **czyta**, nie wystawia.

1. Wejdź na `/finance`. Tabela opłat pokazuje `margin_amount` z `charge`. Przeglądarka nie odejmuje kupna od sprzedaży.
2. Blok „Faktury” listuje `invoice_ref`, `invoice_kind` i `ksef_ref`. Nie ma tu kwoty ani sumy.
3. Nowy dokument albo numer sesji zapisujesz na `/invoices`. Link z tablicy prowadzi tam.

Czego tu nie ma: suma faktur, narracja modelu, silnik limitu, zbiorcze członki. Sprzedaż zostaje na `/charges`. Zapis FV zostaje na `/invoices`.

Nazwy w kodzie: `finance_board` · `sales_invoice` · `invoice_ref` · `ksef_ref`.
