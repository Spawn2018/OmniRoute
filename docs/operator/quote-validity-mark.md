# Operator: quote validity

Katalog HITL dla stanu ważności oferty (`open` / `revised` / `superseded` / `other`).
Zapisujesz kod, `validity_kind` i `source_ref`. To nie jest data na quotation ani numer rewizji.

`amount`, `margin` i `score` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
Nie wpisujesz `valid_until` ani `revision_no` na wycenie. Oferta przetargowa (`tender_quote`) ma własną datę — tu tylko rodzaj stanu.
