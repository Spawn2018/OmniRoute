# Extraction service

## Dozwolone zależności
- `app.repositories.extraction`
- `app.ai_transforms.extraction`
- `app.integrations.docling`
- `app.integrations.langfuse`
- `app.models.extraction_draft`
- `app.domain`

## Zakaz
- zapis `rate_line` / `charge` / `tender_rfp_intake` z tego serwisu (HC-04; 1.3 / G2.9b = warstwa API)
- import `rate_lines` / `charges` / `tender_rfp_intakes` / `tenders` / `inbound_messages` / innych BC services
- wywołanie LLM bez `ExtractionInputGuard`
- logowanie `OPENAI_API_KEY` / treści sekretów z guarda
