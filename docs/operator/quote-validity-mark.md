# Operator: quote validity

Katalog HITL dla stanu ważności oferty (`open` / `revised` / `superseded` / `other`).
Zapisujesz kod, `validity_kind` i `source_ref`. To nie jest data na quotation ani numer rewizji.

`amount`, `margin` i `score` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
Nie wpisujesz tu daty ani numeru rewizji oferty — te pola są na `quotation` (652.0 / 653.0). Oferta przetargowa (`tender_quote`) ma własną datę — tu tylko rodzaj stanu.
