# Linia zamówienia zakupu

Na `/po-lines` dopisujesz **linię SKU** na istniejącym nagłówku zamówienia zakupu: kod linii, SKU, ilość dziesiętną i jednostkę. To nie ASN i nie zlecenie.

1. Najpierw zapisz nagłówek na `/purchase-orders`. Skopiuj jego id.
2. Wejdź na Linię zamówienia. Wklej id nagłówka. Wpisz kod linii (`line_01` — snake 2–32).
3. Podaj SKU, ilość (≥ 0, tekst dziesiętny albo liczba całkowita — nie float przeglądarki) i JM (`pcs`, `kg`).
4. Etykiety zakład / partia / seria / kraj zostaw puste albo wpisz tekst 1–128. To nie są FK.
5. Podaj `source_ref` (`fixture://po-line/…` albo `tenant:manual`).
6. „Zapisz linię zamówienia”. Ten sam kod na tym samym nagłówku albo to samo `source_ref` u tenanta nie wejdzie drugi raz. Cudzy nagłówek nie istnieje.

Czego tu nie ma: ASN, EDI 856, automatyczne zlecenie, kwota. Marża zostaje na `/charges`. Nagłówek zostaje na `/purchase-orders`. Zlecenie zostaje na `/shipments`.

Nazwy w kodzie: `po_line` · `line_code` · `purchase_order_id` · `sku_code` · `qty` · `uom_code` · `source_ref`.
