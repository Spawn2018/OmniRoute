---
name: knowledge-retrieve
description: Pobiera max 8–20 kart z docs/_knowledge/ — nigdy dump całej biblioteki do kontekstu
---

# Knowledge retrieve

Użyj przed planem implementacji, gdy potrzebujesz wzorca zewnętrznego.

## Procedura

1. Określ kategorię: `tools` | `prompts` | `memory-patterns` | `rules-catalog` | `skills-catalog`
2. Przeszukaj `docs/_knowledge/<kategoria>/` po słowach kluczowych zadania.
3. Zwróć **maksymalnie 8–20** najtrafniejszych kart (ścieżka + 3–5 linii streszczenia).
4. **Nigdy** nie wklejaj całego katalogu ani 1000 elementów do kontekstu.

## Zakazy

- RAG na logikę wyceny, schemat DB, reguły VAT — tylko kod/SQL.
- Kopiowanie kodu z kart bez adaptacji do import-linter i AGENTS.md.

## Gdy brak karty

Zgłoś brakującą kartę do dodania przez człowieka. Nie improwizuj architektury.
