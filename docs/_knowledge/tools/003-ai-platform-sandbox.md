# AI platform stack (sandbox)

**Kiedy:** Faza C (C.1–C.5 w kodzie; leftover = vitest HITL / XOR)

| Narzędzie | Rola w OmniRoute | Stan |
|---|---|---|
| instructor | schemat Pydantic z LLM | 0.8 `InstructorExtractor`; **CI = mock** |
| docling | parser PDF A/B | 0.9 `pdf_strings` vs **opcjonalny** pakiet docling |
| langfuse | telemetria promptów | 0.10 trace przy extract; **no-op bez kluczy**; cloud = leftover |
| promptfoo | regresja promptów | 0.10 `just promptfoo` echo w CI; 30 cenników = leftover |

Nie twierdź, że CI odpala żywy OpenAI, transformery llm-guard ani presidio.
Nie ładuj całego katalogu OSS do kontekstu — skill `knowledge-retrieve`.
