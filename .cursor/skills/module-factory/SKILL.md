---
name: module-factory
description: Tworzy nowy moduł domenowy wg matrycy Golden Standard
---

# Module Factory

Każdy moduł w `backend/app/domains/<nazwa>/`:

```
schemas.py       # Pydantic DTO + walidacja wejścia/wyjścia
service.py       # Deterministyczna logika (ZERO AI, ZERO zapisu z LLM)
repository.py    # Dostęp do bazy, SQL na gorących ścieżkach
api.py           # Router FastAPI, mapowanie DTO, uprawnienia OpenFGA
ai_transforms.py # Opcjonalnie: ekstrakcja mail/PDF → JSON (stateless)
```

Frontend: `frontend/src/features/<nazwa>/` — komponenty, hooki, typy, testy.

## Kroki

1. `just new-module <nazwa>` (gdy skrypt gotowy) lub skopiuj z `domains/_template/`.
2. Dodaj wpis w `docs/MODULES.md` i szkielet `docs/spec/<nazwa>.md`.
3. import-linter: moduł nie importuje innych modułów domenowych bez ADR.
4. Pierwszy plaster: migracja + RLS + test izolacji.

## HC

- Zapis stanu tylko przez `service.py`.
- `ai_transforms.py` zwraca propozycję; człowiek zatwierdza przed zapisem.
