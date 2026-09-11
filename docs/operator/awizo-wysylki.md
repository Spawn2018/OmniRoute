# Awizo wysyłki

Na `/asns` dopisujesz **awizo** na istniejącym nagłówku zamówienia zakupu: kod awiza i opcjonalne etykiety. To nie live EDI 856 i nie zlecenie.

1. Najpierw zapisz nagłówek na `/purchase-orders`. Skopiuj jego id.
2. Wejdź na Awizo wysyłki. Wklej id nagłówka. Wpisz kod awiza (`asn_01` — snake 2–32).
3. Jeśli tenant ma egzekucję przewodnika `block_409` (katalog `/routing-guide-enforcements`), wpisz **guide_code** z `/routing-guides`. Brak albo nieznany kod → HTTP 409. Przy samym `record_only` pole możesz zostawić puste.
4. Etykiety zakład / przewoźnik / referencja zostaw puste albo wpisz tekst 1–128. To nie są FK.
5. Podaj `source_ref` (`fixture://asn/…` albo `tenant:manual`).
6. „Zapisz awizo wysyłki”. Ten sam kod na tym samym nagłówku albo to samo `source_ref` u tenanta nie wejdzie drugi raz. Cudzy nagłówek nie istnieje.

Czego tu nie ma: live EDI 856, automatyczne zlecenie, kwota, parser X12, 409 na zleceniu. Marża zostaje na `/charges`. Linia SKU zostaje na `/po-lines`. Zlecenie zostaje na `/shipments`.

Nazwy w kodzie: `asn` · `asn_code` · `guide_code` · `purchase_order_id` · `plant_label` · `carrier_label` · `ship_ref_label` · `source_ref`.
