# Plan realizacji OmniRoute — aktualny (2026-08-31)

**Plan Cursor (pełny):** `.cursor/plans/omniroute-realizacja.plan.md`  
**ADR:** [0001 Cursor factory](adr/0001-cursor-software-factory-weryfikacja.md) · [0002 Frontend 2026](adr/0002-frontend-platform-2026.md)  
**Repo:** https://github.com/Spawn2018/OmniRoute  
**Stan:** Fazy 0+A+A.5+B.2–B.4 done · **0.5 lokalnie** → push → **0.6 DataTableShell** → B.7 → C → D

```mermaid
flowchart LR
  doneB[B_RLS_OpenFGA] --> b5[B5_FrontendShell]
  b5 --> b6[B6_DataTableShell]
  b6 --> phaseC[FazaC_AI]
  phaseC --> phaseD[FazaD_Ops]
```

---

## Ukończone

| Faza | Status |
|------|--------|
| 0 GitHub | ✅ private repo, CI |
| A Cursor OS | ✅ AGENTS, GROUNDING, rules, skills |
| A.5 IDE | ✅ gh + GitHub MCP |
| B.2 RLS 0.3 | ✅ organization, app_user, test izolacji |
| B.3 Gate | ✅ ruff/mypy/pytest/import-linter + PG |
| B.4 OpenFGA 0.4 | ✅ model, require_permission, CI |

---

## Gate dziś vs cel DoD (uczciwość)

Źródło: audyt 2026-08-31. **Nie zamykaj plastra ani nie twierdź „pełny DoD”, jeśli recipe to `echo`.**

| Obietnica | Egzekwowane teraz | Kiedy |
|---|---|---|
| ruff + mypy | ✅ `just check` | — |
| pytest unit + integration | ✅ CI | — |
| import-linter | ✅ `just arch` | — |
| frontend typecheck | ✅ `frontend-typecheck` w gate | — |
| vitest | ✅ `frontend-test` w gate | — |
| cov ≥ 80% | ✅ `test-unit --cov-fail-under=80` | — |
| jscpd ≤ 3% | ✅ `just dup` w gate | — |
| openapi-ts | ✅ `just api-types` + `frontend/src/api/` | regeneruj przy zmianie API |
| size-limit / perf | ❌ stub | po dalszym budgetingu |
| agentlint | ✅ `just agentlint` + baseline | — |
| lazy PostHog | ✅ dynamic `import("posthog-js")` | — |

---

## Faza B — domknięcie

### B.5 Frontend Shell 2026 — delta `0.5-frontend-shell`
- Vite + React 19 + **React Compiler** + Tailwind v4 + shadcn
- TanStack **Router + Query + Form** (+ Table/Virtual w B.6)
- Design tokens (neutral, compact) — anti AI-slop
- Command palette ⌘K · PostHog od dnia 1
- Referencja layoutu: satnaing/shadcn-admin (**wzorce, nie fork**)
- **Dług świadomy 0.5:** ręczny klient API; PostHog w main chunk (~213 kB gzip); auth localStorage (JWT poza zakresem)

### B.6 DataTableShell — delta `0.6-datatable-views`
- ColumnEditor: checkbox + DnD (@dnd-kit / TanStack columnOrder)
- Filtry faceted + URL sync
- ViewManager + tabela `table_view` (RLS)
- Consumer: `tenancy.users`
- UX events PostHog
- **Dodatkowo w 0.6:** vitest minimum na DataTableShell; preferuj start openapi-ts (spłata długu kontraktu)
- Źródła: Pencil & Paper; NN/G; TanStack Column DnD

### B.7 Branch protection (pull-forward z D) — **DONE (procedura)**
- Cel: status check `gate` na `main`
- **Constraint:** GitHub Free + private → API **403**
- **Obowiązuje:** [docs/ops/branch-protection.md](ops/branch-protection.md) (zakaz force-push, green CI przed push)
- Po Pro/Team: włączyć required check `gate` w UI i supersedować procedurę

**TanStack Start:** Thoughtworks **Assess** (2026-04) — **nie** jako fundament; SPA wystarczy.

---

## Faza C — Platforma AI (po B)

### C.1 / 0.7 AI extract HITL hello — **DONE**
- `extraction_draft` RLS · MockExtractor · accept/reject · UI DataTableShell
- Delta: `docs/deltas/archived/0.7-ai-extract-hitl.md`

### C.2 scaffold (równolegle z 0.7) — **DONE**
- docling stub · langfuse no-op · `promptfoo/promptfoo.yaml` · knowledge cards

### C.3 / 0.8 instructor + llm-guard — **DONE**
- Guard na wejściu · InstructorExtractor · provider mock|instructor
- Delta: `docs/deltas/archived/0.8-instructor-llm-guard.md`

### C.4+ (następne)
0.9 docling A/B · 0.10 langfuse/promptfoo CI

## Faza D — Rytm operacyjny — **DONE (minimal)**
- `agentlint` w `just gate` + baseline
- `.github/workflows/pr-nudge.yml` (checklist PR)
- `docs/ops/weekly-refactor.md` + `docs/ops/friday-retrospective.md`
- Bugbot: osobna GitHub App (nie w repo)

---

## Definition of Done (merge)

1. Delta zamknięta; testy zaakceptowane — tylko to, co gate **naprawdę** egzekwuje + kryteria delty
2. `just gate` green (+ integration gdy dotyczy)
3. Łowca duplikatów + review 4-pass
4. CURRENT + PROGRESS zaktualizowane
5. GROUNDING HCs + ADR-0002 (brak drugiego table engine / AI-slop)
6. **WIP:** nie startuj kolejnego plastra przy niezacommitowanym / niepushniętym zakresie bieżącego

## Start

```
/plaster
```

Kontekst: `@docs/state/CURRENT.md` `@docs/PLAN-REALIZACJA.md` `@docs/adr/0002-frontend-platform-2026.md` `@GROUNDING.md`
