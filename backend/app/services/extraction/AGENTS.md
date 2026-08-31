# Extraction service

## Dozwolone zależności
- `app.repositories.extraction`
- `app.ai_transforms.extraction`
- `app.integrations.docling`
- `app.integrations.langfuse`
- `app.models.extraction_draft`
- `app.domain`

## Zakaz
- zapis `rate_line` / `charge` z tego serwisu (HC-04)
- import innych BC services
- wywołanie LLM bez `ExtractionInputGuard`
- logowanie `OPENAI_API_KEY` / treści sekretów z guarda
