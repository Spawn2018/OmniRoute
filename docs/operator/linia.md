# Linia drobnicy

Na `/groupage` zapisujesz katalog linii LTL, nie odcinek na zleceniu i nie magazyn.

1. Na `/locations` zapisz start i koniec jako `postal_zone` albo `address`. Port UN/LOCODE tu nie wchodzi.
2. Wejdź na Linie drobnicy. Podaj `line_code` (snake), oba wskazania, godzinę cutoff (lokalna, dana — system jej nie liczy), `transit_days` (≥ 1) i dni ISODOW (1 = poniedziałek).
3. „Zapisz linię drobnicy” z `source_ref` (`fixture://groupage-line/…` albo `tenant:manual`). Ten sam kod z inną godziną albo TT = nowy wiersz; stary dostaje `superseded_by`. Lista pokazuje tylko bieżące.
4. Oferta kanału z `transit_days` zostaje na `/channel-quotes`. Kalendarz świąt zostaje w ustawieniach. Odcinek na zleceniu zostaje na `/road`.

Czego tu nie ma: OR wielu hubów, WMS, skan paczki, cennik LTL, mapa. Marża zostaje na `/charges`.

Nazwy w kodzie: `groupage_line` · `line_code` · `cutoff_local` · `transit_days` · `operating_dows` · `source_ref`.
