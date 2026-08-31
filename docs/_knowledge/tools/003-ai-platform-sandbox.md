# AI platform stack (sandbox)

**Kiedy:** Faza C (C.1–C.4 w kodzie; 0.10 = langfuse/promptfoo CI)

| Narzędzie | Rola w OmniRoute | Stan |
|---|---|---|
| instructor | schemat Pydantic z LLM | 0.8 `InstructorExtractor`; **CI = mock** |
| docling | parser PDF A/B | 0.9 `pdf_strings` vs **opcjonalny** pakiet docling |
| langfuse | telemetria promptów | no-op bez kluczy — cloud/CI = 0.10+ |
| promptfoo | regresja promptów | plik `promptfoo/promptfoo.yaml`; eval w CI = 0.10+ |

Nie twierdź, że CI odpala żywy OpenAI, transformery llm-guard ani presidio.
Nie ładuj całego katalogu OSS do kontekstu — skill `knowledge-retrieve`.
