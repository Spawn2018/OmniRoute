# Bieżący focus

**Faza:** Bootstrap zakończony (Phase 0 + Phase A)  
**Repo:** https://github.com/Spawn2018/OmniRoute (`main`, zsynchronizowany z `origin/main`)  
**Następny krok:** plaster **0.3** (M-01 RLS Golden Standard) — start Fazy B lub sam plaster wg `docs/spec/tenancy.md` (do utworzenia w Fazie B)

---

# Plaster 0.3 — M-01 Wielodostępność — RLS (Golden Standard)

**Spec:** docs/spec/tenancy.md (do utworzenia w Fazie B)  
**Moduły:** M-01  
**Status:** **następny do realizacji** (Agent mode, `/plaster` lub skill `nowy-plaster`)

## Zakres
Tabela `organization`, `app_user`, polityki RLS, test izolacji jako wzorzec dla wszystkich modułów.

## Poza zakresem
OpenFGA (0.4), outbox (0.4), UI admin tenanta, billing.

## Ustalenia
- RLS wymuszony FORCE ROW LEVEL SECURITY
- Test izolacji kopiowany z `tests/patterns/tenant_isolation.py`

## Kryteria akceptacji
- [ ] Migracja up/down działa
- [ ] Test izolacji tenantów green
- [ ] Brak zapytania bez organization_id w repozytoriach

---

## Ukończone (nie czekać w Plan mode)

| Faza | Co zrobiono |
|---|---|
| **Phase 0** | `git init`, remote `origin`, initial commit + push na GitHub |
| **Phase A** | AGENTS.md, GROUNDING.md, rules, skills, hooks, commands, CI skeleton (`gate.yml`) |

Opcjonalnie później: branch protection na `main` po pierwszym green `gate`; `gh auth` lokalnie jeśli potrzebny CLI.