# Odcinek drobnicy morskiej

Na `/lcl` zostaje lista portów z `is_seaport`. Osobno zapisujesz odcinek na zleceniu — to noga, nie rezerwacja CFS.

1. Zapisz zlecenie na `/shipments`. Dla każdego końca zapisz lokalizację `unlocode` na `/locations` wskazującą port morski (ta tablica albo `/ports`).
2. Wejdź na Drobnica morska. Wklej `shipment_id`, start, koniec i `source_ref` (`fixture://shipment-leg/…` albo `tenant:manual`).
3. „Zapisz odcinek drobnicy” wiąże te wskazania z `leg_kind=ocean_lcl`. Strefa pocztowa albo port bez `is_seaport` odrzuca. Drugi odcinek `ocean_lcl` na to samo zlecenie też.
4. Odcinki `road`, `rail` i `china_rail` zostają osobnymi wierszami. System nie liczy CBM.

Czego tu nie ma: tabela LCL, CFS, rozróżnienie FCL, mapa, HTTP. Marża zostaje na `/charges`.

Nazwy w kodzie: `shipment_leg` · `leg_kind` · `ocean_lcl` · `is_seaport` · `source_ref`.
