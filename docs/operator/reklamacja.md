# Reklamacja ładunku

Na `/claims` zapisujesz reklamację na zleceniu — to zgłoszenie szkody albo niedoboru, nie kwota i nie scoring.

1. Zapisz zlecenie na `/shipments`.
2. Wejdź na Reklamacje ładunku. Wklej `shipment_id`, wybierz rodzaj (`damage` / `shortage` / `other`) i `source_ref` (`fixture://cargo-claim/…` albo `tenant:manual`).
3. „Zapisz reklamację” wiąże te wskazania z wierszem `cargo_claim`. Zły rodzaj albo puste źródło odrzuca. Nieznane zlecenie też.
4. Wyjątek operacyjny zostaje na `/exceptions`. System nie liczy odszkodowania.

Czego tu nie ma: kwota, ubezpieczenie, scoring osoby, oszustwo. Marża zostaje na `/charges`.

Nazwy w kodzie: `cargo_claim` · `claim_kind` · `source_ref`.
