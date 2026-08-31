# Phase 0 — GitHub (bootstrap)

**Status:** lokalny commit gotowy; push zablokowany do gh auth login (Spawn2018)
**Repo (docelowy):** https://github.com/Spawn2018/OmniRoute
**Branch:** main

## Ustalenia Phase 0
- git init -b main w D:\\OMNIROUTE
- Initial commit: Cursor OS, docs, CI skeleton
- Push / gh repo create / branch protection: wymaga zalogowania gh jako Spawn2018

---

# Plaster 0.3 · M-01 Wielodostępność — RLS (Golden Standard)

**Spec:** docs/spec/tenancy.md (do utworzenia w Fazie B)  
**Moduły:** M-01  
**Status:** następny po bootstrapie Cursor OS

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
