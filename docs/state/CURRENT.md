# Bieżący focus

**Faza:** Faza B — plaster 0.3 (M-01 RLS Golden Standard)  
**Repo:** https://github.com/Spawn2018/OmniRoute (`main`)  
**Następny krok:** OpenFGA hello (0.4) / pełny frontend Vite

**Plan Cursor:** Fazy 0+A+A.5 done; B.2 done; B.4/C/D pending.  
**ADR:** [docs/adr/0001-cursor-software-factory-weryfikacja.md](docs/adr/0001-cursor-software-factory-weryfikacja.md)

---

# Plaster 0.3 — M-01 Wielodostępność — RLS (Golden Standard)

**Spec:** [docs/spec/tenancy.md](spec/tenancy.md)  
**Moduły:** M-01  
**Status:** **ukończony** (migracja + test w CI)

## Zakres
Tabela `organization`, `app_user`, polityki RLS FORCE, test izolacji jako wzorzec.

## Kryteria akceptacji
- [x] Migracja up/down zdefiniowana (`001_tenancy_rls`)
- [x] Test izolacji tenantów (CI + `just test-integration`)
- [x] Repozytoria bez jawnego cross-tenant SQL — RLS przez `app.current_org`

---

## Ukończone

| Faza | Co zrobiono |
|---|---|
| **Phase 0** | GitHub Spawn2018/OmniRoute, push, gate.yml |
| **Phase A** | Cursor OS + ADR-0001 |
| **Phase A.5** | gh CLI auth OK, `.env.example`, plan w repo |
| **Phase B.1** | pyproject.toml, FastAPI szkielet, docker-compose |
| **Phase B.2** | Plaster 0.3 RLS + nested AGENTS tenancy |
| **Phase B.3** | Pełny `just gate` (check + test-unit + arch) |

## Następne
- B.4 OpenFGA hello
- Faza C (instructor, docling, langfuse)
- Branch protection po green CI
