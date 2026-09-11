# Audyt frachtu (CT10)

Ekran `/freight-audit-marks` zapisuje rodzaj audytu jako dane: kod snake, rodzaj `expected_vs_invoice` albo `expected_vs_charge`, oraz `source_ref`.

To katalog HITL. Nie porównuje FV z `charge`. Nie liczy drugiej marży.

Źródło: `tenant:manual` albo `fixture://freight-audit-mark/…`.

Czego tu nie ma: silnik audytu, SQL na marży, mapa. Marża zostaje na `/charges`.
