# Dopłata lokalna

Na `/local-charges` zapisujesz **dopłatę** THC, ISPS, seal albo amendment z kwotą Decimal. Opcjonalnie podajesz port UN/LOCODE. To nie extra portowe i nie warning braku.

1. Wejdź na Dopłaty lokalne. Wybierz rodzaj, kwotę i walutę ISO.
2. Zero i float odpadają. Nieznany rodzaj odpada.
3. Port zostaw pusty, gdy dopłata nie jest związana z jednym UN/LOCODE. Zły kod (nie 5 znaków) odpada.
4. „Zapisz dopłatę lokalną” z `source_ref` (`fixture://local-charge/…` albo `tenant:manual`).

Czego tu nie ma: macierz armator×serwis×kontener, FK do katalogu portów, warning braków jako fakt, zapis na `charge`. Marża zostaje na `/charges`. Extra portowe zostają na `/port-surcharges`.

Nazwy w kodzie: `local_charge` · `charge_kind` · `port_unlocode` · `amount` · `currency` · `source_ref`.
