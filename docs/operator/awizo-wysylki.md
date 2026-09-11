# Awizo wysyłki

Na `/asns` dopisujesz **awizo** na istniejącym nagłówku zamówienia zakupu: kod awiza i opcjonalne etykiety. To nie live EDI 856 i nie zlecenie.

1. Najpierw zapisz nagłówek na `/purchase-orders`. Skopiuj jego id.
2. Wejdź na Awizo wysyłki. Wklej id nagłówka. Wpisz kod awiza (`asn_01` — snake 2–32).
3. Jeśli tenant ma egzekucję przewodnika `block_409` (katalog `/routing-guide-enforcements`), wpisz **guide_code** z `/routing-guides`. Brak albo nieznany kod → HTTP 409. Przy samym `record_only` pole możesz zostawić puste.
4. Gdy w `/routing-guide-matches` jest tryb `lane_label` albo `mode_label` **oraz** `block_409`, awizo musi mieć zgodne etykiety: `plant_label` = `lane_label` przewodnika, `carrier_label` = `mode_label` (trim, bez wielkości liter). Sam `guide_code_only` nie dodaje tego kroku.
5. Etykiety zakład / przewoźnik / referencja zostaw puste albo wpisz tekst 1–128 — o ile punkt 4 nie wymaga konkretnej wartości. To nie są FK.
6. Podaj `source_ref` (`fixture://asn/…` albo `tenant:manual`).
7. „Zapisz awizo wysyłki”. Ten sam kod na tym samym nagłówku albo to samo `source_ref` u tenanta nie wejdzie drugi raz. Cudzy nagłówek nie istnieje.
8. Świadoma promocja: wklej `asn_id` i `quotation_id`, „Promuj awizo do zlecenia”. Kopiuje guide/etykiety. Drugi promote tego awiza → konflikt. Nie startuje sam przy zapisie awiza.

Czego tu nie ma: live EDI 856, automatyczne zlecenie przy zapisie awiza, kwota, parser X12. Marża zostaje na `/charges`. Linia SKU zostaje na `/po-lines`. Zlecenie: [zlecenie.md](zlecenie.md).

Nazwy w kodzie: `asn` · `asn_code` · `guide_code` · `purchase_order_id` · `plant_label` · `carrier_label` · `ship_ref_label` · `source_ref` · `routing_guide_match` · `promote` · `shipment.asn_id`.
