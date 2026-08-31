---
name: module-factory
description: Tworzy nowy moduł domenowy wg matrycy Golden Standard
---

# Module Factory

Layout w kodzie (nie `domains/_template/` — tego katalogu nie ma):

```
backend/app/services/<bc>/     # logika; nested AGENTS.md z dozwolonymi deps
backend/app/repositories/      # dostęp SQL
backend/app/api/               # routery FastAPI + require_permission
backend/app/models/            # SQLAlchemy
backend/app/ai_transforms/     # opcjonalnie: extract → JSON (stateless)
```

Wzorzec do kopiowania: `backend/app/services/tenancy/` (fundament) albo
`backend/app/services/extraction/` (HITL).

Frontend: `frontend/src/features/<nazwa>/` — komponenty, hooki, typy, testy.

## Kroki

1. `just new-module` jest **echo (stub, nie DoD)** — skopiuj istniejący BC, nie czekaj na generator.
2. Dodaj wpis w `docs/MODULES.md` i szkielet `docs/spec/<nazwa>.md`.
3. import-linter: moduł nie importuje innych modułów domenowych bez ADR.
4. Pierwszy plaster: migracja + RLS + test izolacji.

## HC

- Zapis stanu tylko przez serwis w `services/<bc>/`.
- `ai_transforms` zwraca propozycję; człowiek zatwierdza przed zapisem.
