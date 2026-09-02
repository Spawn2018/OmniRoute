---
name: knowledge-retrieve
description: Pobiera max 8–20 kart z docs/_knowledge/ — nigdy dump całej biblioteki do kontekstu
---

# Knowledge retrieve

Użyj **albo** skill retrieve, **albo** (preferowane) stdout z
`python scripts/quality/factory_cycle.py --start <plan|plaster|refactor|noc>` —
komendy fabryki odpalają to same.

## Procedura

1. Określ kategorię: `tools` | `prompts` | `memory-patterns` | `rules-catalog` | `skills-catalog`
2. Przeszukaj `docs/_knowledge/<kategoria>/` **oraz** `docs/_knowledge/**/machine-*.md`.
   Przy plasterze: też `docs/_bench/cases/` (poprzedni podobny BC, max kilka kart).
3. Zwróć **maksymalnie 8–20** najtrafniejszych kart (ścieżka + 3–5 linii streszczenia).
4. **Nigdy** nie wklejaj całego katalogu ani 1000 elementów do kontekstu.

## Zakazy

- RAG na logikę wyceny, schemat DB, reguły VAT — tylko kod/SQL.
- Kopiowanie kodu z kart bez adaptacji do import-linter i AGENTS.md.
- Dopisywanie zasad do `AGENTS.md` / `GROUNDING.md` „bo karta tak każe”.

## Gdy brak karty

Nie pytaj operatora. `python scripts/quality/factory_cycle.py --close` dopisze
`machine-*` (RLS/izolacja/bench/powtórzony CI). Nie improwizuj architektury.
