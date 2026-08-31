# Plan realizacji OmniRoute — Build-ready

**Pełny plan Cursor OS:** `.cursor/plans/cursor_software_house_84d0f6a6.plan.md` (lokalnie w IDE)  
**ADR weryfikacji:** [docs/adr/0001-cursor-software-factory-weryfikacja.md](adr/0001-cursor-software-factory-weryfikacja.md)  
**Repo:** https://github.com/Spawn2018/OmniRoute  
**Stan:** Fazy 0+A ukończone · **Build start:** Faza B / plaster 0.3

---

## Ukończone

| Faza | Status |
|------|--------|
| 0 GitHub | repo, push, bootstrap CI (`agent-refs`) |
| A Cursor OS | AGENTS, GROUNDING, rules, skills, hooks, ADR-0001 |

---

## Faza B — NASTĘPNA (Build)

### B.1 Szkielet
- `fastapi/full-stack-fastapi-template` → modularny monolit
- `pyproject.toml` + deps (ruff, mypy, pytest, alembic, import-linter)
- Struktura `backend/app/` + `frontend/src/features/`

### B.2 Plaster 0.3 — M-01 RLS (Golden Standard)
- `docs/deltas/open/0.3-tenancy.md`
- `organization`, `app_user`, RLS FORCE, test izolacji
- Nested `AGENTS.md` w BC tenancy

### B.3 Pełniejszy gate
- `just gate`: rozszerzenie o check/test/arch (gdy jest `pyproject.toml`)
- `gate.yml`: install deps przed `just gate`

### B.4 OpenFGA hello + import-linter

---

## Faza C
instructor, docling A/B, langfuse, promptfoo, `docs/spec/tenancy.md`, `_knowledge/`

## Faza D
Automations PR, refaktor-pass, agentlint CI, branch protection

---

## Start po Build

```
/plaster
```

Kontekst: `@docs/deltas/open/0.3-tenancy.md` `@GROUNDING.md` `@docs/adr/0001-cursor-software-factory-weryfikacja.md`
