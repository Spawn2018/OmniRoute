# Indeks paliwowy

Na `/fuel-indexes` zapisujesz **indeks** FSC, BAF albo CAF z datą publikacji. To nie kurs NBP i nie mnożenie na `charge`.

1. Wejdź na Indeksy paliwowe. Wybierz rodzaj, datę i wartość Decimal (nie float).
2. Zero i float odpadają. Nieznany rodzaj odpada.
3. „Zapisz indeks paliwowy” z `source_ref` (`fixture://fuel-index/…` albo `tenant:manual`).

Czego tu nie ma: przeliczenie SQL na `/charges`, live HTTP, FSC na `nbp_rate`. Marża zostaje na `/charges`. Kurs NBP zostaje na `/nbp-rates`.

Nazwy w kodzie: `fuel_index` · `index_kind` · `published_on` · `index_value` · `source_ref`.
