# Bieżący focus

**Faza:** B — domknięcie frontendu  
**Repo:** https://github.com/Spawn2018/OmniRoute (`main`)  
**Następny krok:** **commit/push 0.5** → green CI → plaster **0.6 DataTableShell**

**Plan:** [docs/PLAN-REALIZACJA.md](docs/PLAN-REALIZACJA.md) (§ Gate dziś vs DoD)  
**ADR:** [docs/adr/0001-cursor-software-factory-weryfikacja.md](docs/adr/0001-cursor-software-factory-weryfikacja.md) · [docs/adr/0002-frontend-platform-2026.md](docs/adr/0002-frontend-platform-2026.md)

---

# Plaster 0.5 — Frontend Shell 2026

**Delta:** [docs/deltas/open/0.5-frontend-shell.md](docs/deltas/open/0.5-frontend-shell.md)  
**Status:** lokalnie gotowy (typecheck+build) — **wymaga commit/push**

## Dostarczone
Vite + React 19/Compiler + TanStack Router/Query/Form + shadcn tokens + shell + ⌘K + PostHog + `/tenancy/users` + `/session`.

## Dług świadomy (nie blokuje zamknięcia 0.5)
Ręczny `frontend/src/lib/api.ts` · PostHog w main chunk · auth localStorage (JWT później)

## Poza zakresem
ColumnEditor / `table_view` (0.6), IdP/JWT, Faza C AI.

---

# Plaster 0.6 — DataTableShell (po push 0.5)

**Delta:** [docs/deltas/open/0.6-datatable-views.md](docs/deltas/open/0.6-datatable-views.md)  
Filtry, widoki, checkbox + DnD, `table_view` RLS · **+ vitest minimum** · preferuj openapi-ts.

---

## Ukończone

| Faza | Co |
|---|---|
| 0–A.5 | GitHub, Cursor OS, MCP |
| B.2–B.4 | RLS, gate (ruff/mypy/pytest/arch), OpenFGA |
| ADR-0002 | Frontend platform 2026 |
| Audyt 2026-08-31 | Gate vs DoD + B.7 constraint (Free private 403) w planie/OS |

## Następne (kolejność bez kolizji)

1. **Commit/push 0.5** + green CI  
2. **0.6** DataTableShell + `table_view` + vitest (+ openapi-ts jeśli mieści się w plastrze)  
3. **B.7** Branch protection gdy Pro/public; inaczej procedura ręczna  
4. Slot jakości: cov-fail-under, jscpd, lazy PostHog (nie równolegle z 0.6)  
5. **Faza C** AI → **Faza D** agentlint / refaktor-pass
