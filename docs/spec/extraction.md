# M-20 — Ekstrakcja dokumentów (HITL)

**Status:** 0.7–0.18 DONE · Charge **1.3** accept → `rate_line` (warstwa API)  
**Delty:** `docs/deltas/archived/0.7-ai-extract-hitl.md`, `0.8-instructor-llm-guard.md`, `0.9-docling-ab.md`, `0.10-langfuse-promptfoo.md`, `0.11-hitl-xor-vitest.md`, `0.12-jwt-session.md`, `0.13-hitl-split.md`, `0.14-http-happy-path.md`, `0.15-t0-document-base64-max.md`, `0.18-http-extract-live-pg.md`, `1.3-accept-rate-line.md`  
**GROUNDING:** HC-03 (`source_ref`, `unparsed_regions`), HC-04 (zero zapisu autonomicznego)

## Zakres (kod dziś)

- Tabela `extraction_draft` + RLS + test izolacji tenantów
- API: list / extract→draft / accept / reject; upload `document_base64` XOR `input_text`
- `document_base64` `max_length=2_666_668` → 422 przed decode
- OpenFGA: `can_review_extractions` na każdym endpoincie `/extractions`
- UI: kolejka DataTableShell + split-screen (podgląd `input_text` | recenzja)
- Provider: `EXTRACTION_PROVIDER=mock` (default CI) | `instructor` (wymaga `OPENAI_API_KEY`)
- Guard: skanery regex przed modelem; pakiet `llm-guard` (transformers) tylko przy `EXTRACTION_LLM_GUARD=true`
- Parser: fingerprint + A (`stub` / `pdf_strings`) vs B (opcjonalny docling); tryb `ab` → `ab_delta_chars`

## Poza zakresem (nie twierdź że jest)

- Zapis `rate_line` / `charge` z `ExtractionService` (1.3: accept → RatesService w API, nie tu)
- Żywy instructor / OpenAI w CI, langfuse cloud, eval promptfoo 30 cenników
- Presidio na każdym endpoincie, outbox, Temporal/Hatchet
- HTTP extract vs live Postgres — 0.18 integration CI (lokalnie PG może wisieć)
- Split-screen PDF canvas / OCR overlay
- Vitest: `extractionCreateBody` (XOR) + `hitlSplitView`; brak RTL całej kolejki

## Kontrakt HITL

1. Model wyciąga dane. Kod nie liczy kwot; payload ma `amount_text`, nie float.
2. Nic nie wchodzi do domeny bez akceptacji człowieka. `ExtractionService.accept` zmienia tylko status draftu.
3. Warstwa API (`AcceptExtractionToRates`) w **tej samej** transakcji HTTP woła `RateLineService.create_buy_rate` (kupno, `source_ref` ze szkicu, `charge_code` z katalogu). Brak poprawnej stawki = rollback całości (fail-closed, komunikat PL).
4. Każdy payload: `source_ref` (nadpisuje serwis z requestu) + `unparsed_regions`.
5. `ExtractionService` nie importuje rates/charges i nie woła LLM bez guarda. Nie outbox / Temporal.

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

- Tożsamość: JWT Bearer (`sub` = `app_user.id`, `org` = `organization_id`). Headery `X-Organization-Id` / `X-User-Id` nie ustalają tenanta.
- Brak/nieważny token → 401; brak `can_review_extractions` → 403
- Router: `backend/app/api/extractions.py` · accept: `AcceptExtractionToRates`
- Serwis: `backend/app/services/extraction/` (bez rates)
- Transformy: `backend/app/ai_transforms/extraction/`
- Parser: `backend/app/integrations/docling/`
- Langfuse: no-op bez kluczy; przy extract — trace bez `input_text` (`app.integrations.langfuse`)
- Promptfoo: `promptfoo/promptfoo.yaml` echo w CI (`just promptfoo`); pytest fixture’e MockExtractor

## UI

- Kolejka: `frontend/src/features/extraction/queue-page.tsx` na DataTableShell
- Split-screen: `hitl-review-split.tsx` — podgląd źródła | kandydaci + accept/reject
- Typy: `just api-types` → `frontend/src/api/`; wrapper rzutuje `ExtractRequest` (flatten anyOf|null)

## Kryteria 0.7–0.14 (spełnione)

- Test izolacji `extraction_draft`; accept HTTP → `rate_line` w tej samej transakcji (1.3)
- Guard przed ekstraktorem; CI = mock
- PDF bez docling → `pdf_strings`; A/B zapisuje deltę znaków
- Trace langfuse przy extract; bez kluczy no-op; metadane bez `input_text`
- promptfoo echo w CI (`just promptfoo` = pytest, nie npx); te same fixture’e MockExtractor
- HTTP XOR 422; vitest `extractionCreateBody`
- `document_base64` max_length → 422 przed decode (0.15 T0)
- HTTP happy-path (0.14): extract/list/accept/reject unit + stub serwisu
- HTTP extract live PG (0.18): 201 + token A / draft B → 404; integration CI
- Charge 1.3: accept + `rate_line` w jednej transakcji HTTP; `ExtractionService` bez importu rates
- `just gate` green (unit); integration OpenFGA/RLS/0.18/1.3 w CI

## Następny leftover

Auth0 I1. Wave FE U-* otwarte (ta strona HITL nie zamyka fali).
Presidio i żywy llm-guard = później.
Nie startuj kolejnego plastra przy niepushniętym WIP.

### Poza 0.14 (zostaje)

- HTTP extract vs live Postgres — 0.18 testy integration (CI)
- Split-screen PDF canvas / OCR overlay
- Cloud Langfuse jako wymóg merge
- 30 cenników eval (osobna decyzja danych)
- Presidio na wszystkich endpointach API
- Leftovery: [docs/ops/docs-debt.md](../ops/docs-debt.md)
