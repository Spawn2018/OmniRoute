# Reklamacja ładunku

Na `/claims` zapisujesz reklamację na zleceniu — to zgłoszenie szkody albo niedoboru, nie kwota i nie scoring.

1. Zapisz zlecenie na `/shipments`.
2. Wejdź na Reklamacje ładunku. Wklej `shipment_id`, wybierz rodzaj (`damage` / `shortage` / `other`), kod OS&D (`overage` / `shortage` / `damage` / `loss`), okno zawiadomienia CMR (`notice_7` albo `notice_21`) oraz dwa dni: zawiadomienie i pozew. Zaznacz dowody, które masz: GPS, temperatura, zdjęcie (niezależne checkboxy). `source_ref` to `fixture://cargo-claim/…` albo `tenant:manual`.
3. „Zapisz reklamację” wiąże te wskazania z wierszem `cargo_claim`. Zły rodzaj, kod OS&D, okno albo data odrzuca. Pozew przed zawiadomieniem też. Nieznane zlecenie też.
4. Dni 7/21/365 wpisujesz sam z konwencji. System nie dodaje ich do daty dostawy i nie pobiera GPS ani bajtów zdjęcia.

Czego tu nie ma: kwota, ubezpieczenie, scoring osoby, oszustwo, silnik terminów, live GPS, upload zdjęć. Marża zostaje na `/charges`.

Nazwy w kodzie: `cargo_claim` · `claim_kind` · `damage_code` · `cmr_notice_window` · `notice_due_at` · `suit_due_at` · `evidence_gps` · `evidence_temp` · `evidence_photo` · `source_ref`.
