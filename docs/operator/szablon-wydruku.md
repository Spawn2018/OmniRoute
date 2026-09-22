# Szablon wydruku

Na `/document-templates` zapisujesz **wskazanie layoutu** etykiety własnej albo CMR. To nie PDF i nie etykieta obcej sieci.

1. Wejdź na Szablony wydruku. Wybierz `template_kind` (`own_label` / `cmr`), język (`pl` / `en`) i wyjście `html_print`.
2. Podaj `layout_ref` (snake, 2–64). To nazwa układu, nie plik.
3. Opcjonalnie podaj `branding_ref` (snake, 2–64) — wskazanie marki/logo tenanta, nie upload i nie URL.
4. „Zapisz szablon wydruku” z `source_ref` (`fixture://document-template/…` albo `tenant:manual`).

Czego tu nie ma: PDF/ZPL, QR `shipment_ref`, 409 wyjazdu, etykieta Palletforce, marża.

Nazwy w kodzie: `document_template` · `template_kind` · `layout_ref` · `branding_ref` · `output_kind` · `source_ref`.
