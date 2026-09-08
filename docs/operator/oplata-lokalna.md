# Dopłata lokalna

Na `/local-charges` zapisujesz **dopłatę** THC, ISPS, seal albo amendment z kwotą Decimal. To nie extra portowe i nie warning braku.

1. Wejdź na Dopłaty lokalne. Wybierz rodzaj, kwotę i walutę ISO.
2. Zero i float odpadają. Nieznany rodzaj odpada.
3. „Zapisz dopłatę lokalną” z `source_ref` (`fixture://local-charge/…` albo `tenant:manual`).

Czego tu nie ma: macierz armator×port, warning braków jako fakt, zapis na `charge`. Marża zostaje na `/charges`. Extra portowe zostają na `/port-surcharges`.

Nazwy w kodzie: `local_charge` · `charge_kind` · `amount` · `currency` · `source_ref`.
