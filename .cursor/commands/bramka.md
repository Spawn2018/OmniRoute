---
description: Pełna weryfikacja plastra
---

Uruchom subagenta `weryfikator` z:
- ścieżką do delta-spec
- listą zmienionych plików (`git diff --name-only main`)

Następnie subagenta `audytor-wydajnosci`, jeśli zmieniły się zapytania.

Zwróć tabelę: kryterium → PRZESZŁO / NIE / NIE DA SIĘ SPRAWDZIĆ.
Przy NIE — dokładny komunikat, bez interpretacji.

Nie naprawiaj niczego w tym kroku.
