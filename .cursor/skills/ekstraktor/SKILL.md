---
name: ekstraktor
description: Pipeline ekstrakcji cenników i dokumentów M-20
---

# Pipeline ekstrakcji

## Cztery reguły twarde
1. Model nie licza. Żadnych sum, przeliczeń, mnożenia.
2. Model nie zapisuje. Wszystko przez kolejkę review.
3. Bez `source_ref` rekord nie wchodzi do bazy.
4. `unparsed_regions` obowiązkowe w schemacie odpowiedzi.

## Kolejność
1. fingerprint układu → parser deterministyczny
2. dopiero potem instructor + docling

## Bezpieczeństwo
`llm-guard` + `presidio`. promptfoo na 30 cennikach przy zmianie promptu.

## Pomiar
Każda zmiana → liczba przed/po. Bez liczby nie merge.
