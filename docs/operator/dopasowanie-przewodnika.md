# Dopasowanie przewodnika (CT4 leftover)

Ekran `/routing-guide-matches` zapisuje tryb dopasowania jako dane: kod snake, rodzaj `guide_code_only` / `lane_label` / `mode_label`, oraz `source_ref`.

Przy `block_409` na ASN katalog wpływa na bramkę: `lane_label` / `mode_label` porównują etykiety awiza z przewodnikiem. `guide_code_only` zostaje przy samym kodzie. Zlecenie (`/shipments`) w tym leftoverze nadal tylko equality `guide_code`.

Źródło: `tenant:manual` albo `fixture://routing-guide-match/…`.

Czego tu nie ma: fuzzy/LLM, matching na shipment, mapa. Marża na `/charges`.
