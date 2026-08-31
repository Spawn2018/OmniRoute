# Instructor + llm-guard (0.8)

**Kiedy:** M-20 ekstrakcja po HITL hello

## Kontrakt

1. Guard skanuje `input_text` **przed** modelem (injection, sekrety).
2. Instructor wymusza `ExtractionPayload`; `source_ref` nadpisuje serwis.
3. CI: `EXTRACTION_PROVIDER=mock`. Żywy LLM tylko z `OPENAI_API_KEY`.
4. Pakiet `llm-guard` (ML) jest opcjonalny — default to skanery regex.

Kod: `backend/app/ai_transforms/extraction/{input_guard,instructor_extractor,provider}.py`
