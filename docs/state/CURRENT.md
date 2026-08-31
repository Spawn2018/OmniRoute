# Bieżący focus

**Faza:** Faza B — plaster 0.4 (OpenFGA hello)  
**Repo:** https://github.com/Spawn2018/OmniRoute (`main`)  
**Następny krok:** frontend Vite / Faza C

**Plan Cursor:** Fazy 0+A+A.5 done; B.1–B.4 done; C/D pending.  
**ADR:** [docs/adr/0001-cursor-software-factory-weryfikacja.md](docs/adr/0001-cursor-software-factory-weryfikacja.md)

---

# Plaster 0.4 — OpenFGA hello

**Delta:** [docs/deltas/open/0.4-openfga.md](docs/deltas/open/0.4-openfga.md)  
**Spec:** [docs/spec/tenancy.md](docs/spec/tenancy.md)  
**Moduły:** M-01  
**Status:** **ukończony** (skill + compose + model + API + CI green)

## Zakres
- OpenFGA w docker-compose + CI
- Model: `organization.member` → `can_list_users`
- `require_permission` na `GET /tenancy/users`
- Skill `openfga-change`

## Kryteria akceptacji
- [x] Endpoint bez uprawnienia → 403
- [x] Unit gate lokalnie
- [x] Integration OpenFGA green w CI

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
| **Phase B.4** | OpenFGA hello (model, klient, require_permission) |

## Następne
- Faza C (instructor, docling, langfuse)
- Frontend Vite pełny
- Branch protection po green CI
