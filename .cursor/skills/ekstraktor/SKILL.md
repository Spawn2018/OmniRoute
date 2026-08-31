---
name: ekstraktor
description: Pipeline ekstrakcji cenników i dokumentów M-20
---

# Pipeline ekstrakcji

## Cztery reguły twarde
1. Model nie liczy. Żadnych sum, przeliczeń, mnożenia.
2. Model nie zapisuje. Wszystko przez kolejkę review (`extraction_draft`).
3. Bez `source_ref` rekord nie wchodzi do bazy.
4. `unparsed_regions` obowiązkowe w schemacie odpowiedzi.

## Stan kodu (nie wizja)
- CI default: `MockExtractor` (`EXTRACTION_PROVIDER=mock`).
- `EXTRACTION_PROVIDER=instructor` wymaga `OPENAI_API_KEY` — nie w CI.
- Guard: skanery regex, chyba że `EXTRACTION_LLM_GUARD=true` (pakiet transformers).
- Docling A/B: plaster 0.9 (`EXTRACTION_PARSER=stub|pdf_strings|docling|ab`).
- Presidio + promptfoo na 30 cennikach + langfuse cloud = **po 0.10**, nie zrobione.
- 0.10: trace langfuse przy extract (no-op bez kluczy); `just promptfoo` echo w CI.
- Nie twierdź, że CI odpala żywe transformery llm-guard.

## Kolejność
1. fingerprint układu → parser deterministyczny
2. dopiero potem instructor + docling (gdy provider/parser to włączają)

## Pomiar
Każda zmiana A/B → `ab_delta_chars` (lub inna liczba przed/po). Bez liczby nie merge.

Spec: `docs/spec/extraction.md`.
