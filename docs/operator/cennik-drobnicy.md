# Cennik drobnicy

Na `/groupage-tariffs` zapisujesz **próg wagi** na strefie taryfowej (`location` rodzaju `postal_zone`). Kwota to Decimal z walutą. To nie silnik wyceny.

1. Na `/locations` zapisz strefę `postal_zone` (nie UN/LOCODE, nie adres).
2. Wejdź na Cennik drobnicy. Podaj `tariff_code` (snake), `location_id` strefy, próg `chargeable_weight` i kwotę kupna z walutą ISO.
3. Port albo adres na `location` odpada — to nie strefa LTL. Zero i float na wadze albo kwocie odpadają.
4. „Zapisz próg cennika drobnicy” z `source_ref` (`fixture://groupage-tariff/…` albo `tenant:manual`).

Czego tu nie ma: matching WHEN/IF (P1), T-SQL, objętość, paleta, FSC, marża. Marża zostaje na `/charges`. Wycena ze stawek zostaje na `/rate-lines`. `chargeable_weight` tu jest progiem-daną, nie wyliczeniem.

Nazwy w kodzie: `groupage_tariff` · `tariff_code` · `chargeable_weight` · `amount` · `currency` · `source_ref`.
