# Konosament LCL (HBL/MBL)

Na `/ocean-bills` zapisujesz **numer** HBL albo MBL na zleceniu. To nie PDF i nie booking armatora.

1. Zapisz zlecenie na `/shipments`.
2. Na `/organization-settings` ustaw `hbl_number_prefix` i `mbl_number_prefix` (1–16 znaków A–Z 0–9 . _ -), tak jak prefiks oferty albo HAWB.
3. Wejdź na Konosament. Wklej `shipment_id`, wybierz `hbl` albo `mbl`, opcjonalnie wklej numer ręcznie (2–32 litery, cyfry, myślnik) albo zostaw puste.
4. „Zapisz konosament” z `source_ref` (`fixture://ocean-bill/…` albo `tenant:manual`).
5. Na liście przy pustym numerze „Nadaj HBL” / „Nadaj MBL” bierze prefiks z ustawień i dopisuje cztery cyfry (kolejny numer liczy baza, osobno dla HBL i MBL). Drugie kliknięcie nie zmienia numeru. Brak prefiksu albo zły rodzaj listu odrzuca.
6. Konsolidacja wielu house pod jeden MBL zostaje poza tym ekranem.

Czego tu nie ma: PDF, booking armatora, HTTP, cyfra kontrolna. Marża zostaje na `/charges`.

Nazwy w kodzie: `ocean_bill` · `bill_no` · `bill_kind` · `hbl_number_prefix` · `mbl_number_prefix` · `source_ref`.
