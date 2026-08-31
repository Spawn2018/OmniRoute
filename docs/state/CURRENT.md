# Bieżący focus

**Faza:** Bootstrap zakończony (Phase 0 + Phase A); plan zsynchronizowany  
**Repo:** https://github.com/Spawn2018/OmniRoute (`main`)  
**Ostatnie commity:** `58facbd` (bootstrap CI gate), `e21ac45` (ADR-0001)  
**Następny krok:** plaster **0.3** (M-01 RLS Golden Standard) — start Fazy B

**Plan Cursor:** Fazy 0+A = completed; B/C/D = pending.  
**ADR:** [docs/adr/0001-cursor-software-factory-weryfikacja.md](../adr/0001-cursor-software-factory-weryfikacja.md)

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
- `just gate` do Fazy B = tylko `agent-refs`; pełny gate po `pyproject.toml`

## Kryteria akceptacji
- [ ] Migracja up/down działa
- [ ] Test izolacji tenantów green
- [ ] Brak zapytania bez organization_id w repozytoriach

---

## Ukończone

| Faza | Co zrobiono |
|---|---|
| **Phase 0** | GitHub Spawn2018/OmniRoute, push, gate.yml |
| **Phase A** | Cursor OS + ADR-0001 (weryfikacja Gemini/ChatGPT/nauka) |
| **CI fix** | Bootstrap gate: `just gate` → agent-refs (bez ruff do Fazy B) |

Opcjonalnie: branch protection na `main` po green `gate`.
