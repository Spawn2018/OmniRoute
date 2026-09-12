# Operator: kod języka

Katalog HITL dla kodu języka na zleceniu (`pl` / `en` / `de` / `other`).
Zapisujesz kod, `locale_kind` i `source_ref`. To nie jest mutacja i18n UI ani `preferred_language` na party.

`amount`, `margin` i `score` są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
Nie mutujesz kolumny na shipment ani ustawień języka interfejsu.
