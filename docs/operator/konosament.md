# Konosament LCL

Na `/ocean-bills` zapisujesz **numer** HBL albo MBL na zleceniu. To nie PDF i nie booking armatora.

1. Na `/shipments` zapisz zlecenie. Odcinek `ocean_lcl` zostaje na `/lcl` — ten ekran go nie duplikuje.
2. Wejdź na Konosament LCL. Podaj `bill_no` (2–32 litery, cyfry, myślnik) i rodzaj (`hbl` / `mbl`).
3. „Zapisz konosament” z `source_ref` (`fixture://ocean-bill/…` albo `tenant:manual`).

Czego tu nie ma: PDF, pula numerów M-03, konsolidacja wielu house pod jeden master, live HTTP HZ/S21, HAWB.

Nazwy w kodzie: `ocean_bill` · `bill_no` · `bill_kind` · `source_ref`.
