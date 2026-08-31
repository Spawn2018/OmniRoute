# M-20 — Ekstrakcja dokumentów (HITL)

**Status:** 0.7–0.11 DONE · następny leftover: JWT  
**Delty:** `docs/deltas/archived/0.7-ai-extract-hitl.md`, `0.8-instructor-llm-guard.md`, `0.9-docling-ab.md`, `0.10-langfuse-promptfoo.md`, `0.11-hitl-xor-vitest.md`  
**GROUNDING:** HC-03 (`source_ref`, `unparsed_regions`), HC-04 (zero zapisu autonomicznego)

## Zakres (kod dziś)

- Tabela `extraction_draft` + RLS + test izolacji tenantów
- API: list / extract→draft / accept / reject; upload `document_base64` XOR `input_text`
- OpenFGA: `can_review_extractions` na każdym endpoincie `/extractions`
- UI: kolejka DataTableShell + formularz (nie split-screen podgląd | formularz)
- Provider: `EXTRACTION_PROVIDER=mock` (default CI) | `instructor` (wymaga `OPENAI_API_KEY`)
- Guard: skanery regex przed modelem; pakiet `llm-guard` (transformers) tylko przy `EXTRACTION_LLM_GUARD=true`
- Parser: fingerprint + A (`stub` / `pdf_strings`) vs B (opcjonalny docling); tryb `ab` → `ab_delta_chars`

## Poza zakresem (nie twierdź że jest)

- Zapis `rate_line` / `charge` z serwisu ekstrakcji
- Żywy instructor / OpenAI w CI, langfuse cloud, eval promptfoo 30 cenników
- Presidio na każdym endpoincie, outbox, Temporal/Hatchet
- Split-screen HITL, JWT zamiast headerów sesji
- Vitest: `extractionCreateBody` (XOR plik/tekst); brak RTL całej kolejki / split-screen

## Kontrakt HITL

1. Model wyciąga dane. Kod nie liczy kwot; payload ma `amount_text`, nie float.
2. Nic nie wchodzi do domeny bez akceptacji człowieka. Accept/reject zmienia tylko status draftu.
3. Każdy payload: `source_ref` (nadpisuje serwis z requestu) + `unparsed_regions`.
4. `ExtractionService` nie importuje innych BC i nie woła LLM bez guarda.

## Provider i guard

| Zmienna | Domyślnie | Znaczenie |
|---|---|---|
| `EXTRACTION_PROVIDER` | `mock` | CI: `MockExtractor`. `instructor` = żywy LLM |
| `EXTRACTION_LLM_GUARD` | `false` | `true` wymaga pakietu `llm-guard` |
| `EXTRACTION_PARSER` | `stub` | `pdf_strings` / `docling` / `ab` |

CI nie odpala transformerów llm-guard ani OpenAI.

## Docling A/B (0.9)

- `layout_fingerprint`: pdf vs text
- A wygrywa w CI bez pakietu docling
- `EXTRACTION_PARSER=docling` bez pakietu → błąd domenowy
- Tryb `ab`: dłuższy tekst; w payloadzie `parser_name` + `ab_delta_chars`

## AuthZ i API

- Brak `can_review_extractions` → 403
- Router: `backend/app/api/extractions.py`
- Serwis: `backend/app/services/extraction/`
- Transformy: `backend/app/ai_transforms/extraction/`
- Parser: `backend/app/integrations/docling/`
- Langfuse: no-op bez kluczy; przy extract — trace bez `input_text` (`app.integrations.langfuse`)
- Promptfoo: `promptfoo/promptfoo.yaml` echo w CI (`just promptfoo`); pytest fixture’e MockExtractor

## UI

- Kolejka: `frontend/src/features/extraction/queue-page.tsx` na DataTableShell
- Split-screen HITL = backlog UX, nie obecny kanon
- Typy: `just api-types` → `frontend/src/api/`; wrapper rzutuje `ExtractRequest` (flatten anyOf|null)

## Kryteria 0.7–0.10 (spełnione)

- Test izolacji `extraction_draft`; accept ≠ `rate_line`
- Guard przed ekstraktorem; CI = mock
- PDF bez docling → `pdf_strings`; A/B zapisuje deltę znaków
- Trace langfuse przy extract; bez kluczy no-op; metadane bez `input_text`
- promptfoo echo w CI (`just promptfoo` = pytest, nie npx); te same fixture’e MockExtractor
- HTTP XOR 422; vitest `extractionCreateBody`
- `just gate` green (unit); integration OpenFGA/RLS w CI

## Następny leftover

JWT zamiast headerów sesji. Presidio i żywy llm-guard = później.
Nie startuj kolejnego plastra przy niepushniętym WIP.

### Poza 0.11 (zostaje)

- Cloud Langfuse jako wymóg merge
- 30 cenników eval (osobna decyzja danych)
- Presidio na wszystkich endpointach API
- HTTP happy-path extract/accept/reject, JWT, split-screen — [docs/ops/docs-debt.md](../ops/docs-debt.md)
