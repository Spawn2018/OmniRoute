# Tablica finansowa

Marża, kurs NBP i limit kontrahenta to fakty z katalogów. Faktura sprzedaży to osobny wiersz — tablica go **czyta**, nie wystawia. Narracja powtarza te fakty zdaniami. Model ich nie liczy.

1. Wejdź na `/finance`. Tabela opłat pokazuje `margin_amount` z GET `/charges` (różnica sell−buy w SQL). Przeglądarka nie odejmuje kupna od sprzedaży.
2. Na `/charges` pole „Zlecenie” jest opcjonalne: wklejasz identyfikator zlecenia tego tenanta albo zostawiasz puste. Puste zostaje puste. Obce zlecenie nie wchodzi.
3. Tabela „Marża drzewa” na `/charges` czyta GET `/charges/tree-margins`. To suma kupna, sprzedaży i marży zlecenia głównego oraz jego bezpośrednich podzleceń, policzona w SQL, osobno dla każdej waluty. Przeglądarka nie dodaje kwot. Wnuki i opłata bez zlecenia nie wchodzą.
4. Blok „Faktury” listuje `invoice_ref`, `invoice_kind` i `ksef_ref`. Nie ma tu kwoty ani sumy.
5. Nowy dokument albo numer sesji zapisujesz na `/invoices`. Link z tablicy prowadzi tam.
6. „Narracja po SQL” składa zdania z tych samych wierszy. Nie ma sumy faktur i nie ma komentarza modelu.

Czego tu nie ma: suma faktur, asystent liczący, silnik limitu, zbiorcze członki. Sprzedaż zostaje na `/charges`. Zapis FV zostaje na `/invoices`.

Nazwy w kodzie: `finance_board` · `sales_invoice` · `invoice_ref` · `ksef_ref`.
