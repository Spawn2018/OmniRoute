# Knowledge Library

Curated wzorce — **nigdy** ładuj całości do kontekstu Cursor.

Agent używa skill `knowledge-retrieve` → max 8–20 kart.
Karty `machine-*.md` dopisuje `/zamknij` (`craft_close.py`), nie operator.
Korpus rzemiosła: `docs/_bench/cases/`.

## Kategorie

- `tools/` — integracje, CLI, mapa `just gate` (`006-just-gate-mapa.md`), skąd schemat (`008-schemat-bazy-skad.md`)
- `prompts/` — wzorce promptów ekstrakcji, nie logika biznesowa
- `memory-patterns/` — RAG, pgvector, kiedy tak/nie; `machine-*` z orakulum RLS/izolacja
- `rules-catalog/` — **puste** — nie dumpuj tu 500 reguł
- `skills-catalog/` — **puste** — nie dumpuj tu procedur


## Źródła do kuracji

- `Informacje z claude/katalog-repozytoriow.md`
- `Informacje z claude/72-repozytoriow-github.md`
- Consensus / Gemini audyt — tylko streszczenia, nie raw dump

Dodawaj karty jako pojedyncze pliki `.md` (≤80 linii).
