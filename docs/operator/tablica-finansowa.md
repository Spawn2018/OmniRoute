# Tablica finansowa

Marża, kurs NBP i limit kontrahenta to fakty z katalogów. Faktura sprzedaży to osobny wiersz — tablica go **czyta**, nie wystawia. Narracja powtarza te fakty zdaniami. Model ich nie liczy.

1. Wejdź na `/finance`. Tabela opłat pokazuje `margin_amount` z `charge`. Przeglądarka nie odejmuje kupna od sprzedaży.
2. Blok „Faktury” listuje `invoice_ref`, `invoice_kind` i `ksef_ref`. Nie ma tu kwoty ani sumy.
3. Nowy dokument albo numer sesji zapisujesz na `/invoices`. Link z tablicy prowadzi tam.
4. „Narracja po SQL” składa zdania z tych samych wierszy. Nie ma sumy faktur i nie ma komentarza modelu.

Czego tu nie ma: suma faktur, asystent liczący, silnik limitu, zbiorcze członki. Sprzedaż zostaje na `/charges`. Zapis FV zostaje na `/invoices`.

Nazwy w kodzie: `finance_board` · `sales_invoice` · `invoice_ref` · `ksef_ref`.
