# Zamówienie zakupu

Na `/purchase-orders` dopisujesz **nagłówek zamówienia zakupu** tenanta: kod snake oraz opcjonalną etykietę zakładu. To nie linia SKU, nie ASN i nie zlecenie.

1. Wejdź na Zamówienie zakupu. Wpisz kod (`po_gdansk_01` — snake 2–32).
2. Zakład zostaw pusty albo wpisz etykietę (tekst 1–128). To nie jest FK do geography.
3. Podaj `source_ref` (`fixture://purchase-order/…` albo `tenant:manual`).
4. „Zapisz zamówienie zakupu”. Ten sam kod albo to samo `source_ref` u tenanta nie wejdzie drugi raz.

Czego tu nie ma: `po_line`, SKU, qty, ASN, EDI 856, automatyczne zlecenie, kwota. Marża zostaje na `/charges`. Zlecenie zostaje na `/shipments`. Przeniesienie pól oferty zostaje na `/quotations`.

Nazwy w kodzie: `purchase_order` · `po_code` · `plant_label` · `source_ref`.
