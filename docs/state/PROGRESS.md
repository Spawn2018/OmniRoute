# Historia plastrów

| Data | Plaster | Moduł | Opis |
|---|---|---|---|
| 2026-08-31 | Phase 0 | — | GitHub: repo Spawn2018/OmniRoute, init, initial commit, push na origin/main |
| 2026-08-31 | Phase A | — | Bootstrap Cursor OS: AGENTS.md, GROUNDING.md, rules, skills, hooks, gate.yml |
| 2026-08-31 | ADR-0001 | — | Weryfikacja Cursor factory (Gemini/ChatGPT/nauka) → docs/adr |
| 2026-08-31 | CI fix | — | Bootstrap gate: agent-refs only do Fazy B (58facbd) |
| 2026-08-31 | Plan sync | — | Plan Cursor zsynchronizowany ze stanem repo |
| 2026-08-31 | Phase A.5 | — | gh CLI auth, .env.example, plan w .cursor/plans/ |
| 2026-08-31 | Phase B.1 | — | pyproject.toml, FastAPI, docker-compose, alembic |
| 2026-08-31 | 0.3 | M-01 | RLS Golden Standard: organization, app_user, test izolacji |
| 2026-08-31 | Phase B.3 | — | Pełny gate: ruff, mypy, pytest-unit, import-linter + CI postgres |
| 2026-08-31 | 0.4 | M-01 | OpenFGA hello: model, klient, require_permission, CI green |
| 2026-08-31 | ADR-0002 | — | Frontend platform 2026 (Thoughtworks/SoR/NN/G) + DataTableShell |
| 2026-08-31 | Audyt | — | Gate vs DoD + B.7 Free/403 wciągnięte do planu, AGENTS, skills, rules |
| 2026-08-31 | 0.5 | UI | Frontend Shell: Vite, Compiler, TanStack R/Q/Form, shadcn, ⌘K, PostHog, /tenancy/users |
| 2026-08-31 | 0.6 | UI/M-01 | DataTableShell + table_view RLS + ColumnEditor DnD + ViewManager + vitest |
| 2026-08-31 | B.7 | ops | Branch protection: procedura ręczna (Free private 403) — docs/ops/branch-protection.md |
| 2026-08-31 | Jakość | — | openapi-ts + cov≥80% + jscpd≤3% w gate + lazy PostHog |
| 2026-08-31 | 0.7 | M-20 | AI extract HITL: extraction_draft RLS, MockExtractor, OpenFGA, UI queue |
| 2026-08-31 | Faza C scaffold | AI | docling stub, langfuse no-op, promptfoo.yaml, knowledge cards |
| 2026-08-31 | Faza D | ops | agentlint w gate, pr-nudge.yml, weekly-refactor + friday-retrospective |
| 2026-08-31 | 0.8 | M-20 | instructor + llm-guard: schemat Pydantic, guard przed modelem, CI=mock |
| 2026-08-31 | 0.9 | M-20 | docling A/B: fingerprint, pdf_strings vs docling, ab_delta_chars, upload |
| 2026-08-31 | docs/OS | — | Honesty sync: PLAN/README/ARCHITECTURE/MODULES/ADR/skills/rules + spec M-20; delty 0.3/0.4 archived; `just test` bez `|| true`; leftovery audytu w PLAN + docs-debt.md |
| 2026-08-31 | 0.10 | M-20 | langfuse trace przy extract (no-op bez kluczy) + `just promptfoo` pytest echo |
| 2026-08-31 | ops | — | Pętla po każdym kroku: docs/ops/post-plaster.md (pomiar → naprawa → docs-debt) |
| 2026-08-31 | 0.11 | M-20 | HTTP XOR 422 + vitest extractionCreateBody (kolejka HITL) |
| 2026-08-31 | 0.12 | M-01 | JWT HS256 session: Bearer claims, nie spoofowalne headery |
| 2026-08-31 | 0.13 | M-20 | split-screen HITL: podgląd input_text \| recenzja kandydatów |
| 2026-08-31 | 0.14 | M-20 | HTTP happy-path extract/list/accept/reject (JWT, stub serwisu) |
| 2026-08-31 | docs/OS | — | kanon `/testy` `/bramka` zamiast person z archiwum |
| — | leftover | M-01 | **Następny:** OAuth/OIDC / hasła |
