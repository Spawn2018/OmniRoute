# Przewodnik routingu

Na `/routing-guides` dopisujesz **przewodnik** jako katalog: kod i opcjonalne etykiety korytarza/trybu. To nie blokuje zlecenia (409) i nie jest mapą.

1. Wejdź na Przewodnik routingu. Wpisz kod (`guide_pl_de` — snake 2–32).
2. Etykiety korytarz / tryb zostaw puste albo wpisz tekst 1–128. To nie są FK.
3. Podaj `source_ref` (`fixture://routing-guide/…` albo `tenant:manual`).
4. „Zapisz przewodnik routingu”. Ten sam kod albo to samo `source_ref` u tenanta nie wejdzie drugi raz.

Czego tu nie ma: 409 na zlecenie, auto shipment, OTIF, live EDI, mapa. Marża zostaje na `/charges`.

Nazwy w kodzie: `routing_guide` · `guide_code` · `lane_label` · `mode_label` · `source_ref`.
