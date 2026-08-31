# AI platform stack (sandbox)

**Kiedy:** Faza C

| Narzędzie | Rola w OmniRoute | Stan |
|---|---|---|
| instructor | schemat Pydantic z LLM | 0.8 `InstructorExtractor` (CI = mock) |
| docling | parser PDF A/B | 0.9 stub/`pdf_strings` vs opcjonalny docling |
| langfuse | telemetria promptów | no-op bez kluczy |
| promptfoo | regresja promptów | `promptfoo/promptfoo.yaml` |

Nie ładuj całego katalogu OSS do kontekstu — skill `knowledge-retrieve`.
