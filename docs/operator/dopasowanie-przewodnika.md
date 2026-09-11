# Dopasowanie przewodnika (CT4 leftover)

Ekran `/routing-guide-matches` zapisuje tryb dopasowania jako dane: kod snake, rodzaj `guide_code_only` / `lane_label` / `mode_label`, oraz `source_ref`.

To katalog HITL. Nie porównuje korytarza ani trybu przy zapisie ASN/zlecenia. Bramka 409 zostaje na equality `guide_code`.

Źródło: `tenant:manual` albo `fixture://routing-guide-match/…`.

Czego tu nie ma: silnik matching, zmiana 409, mapa. Marża na `/charges`.
