# OmniRoute

Wielodostępna platforma spedycyjna (LOGMAR Sp. z o.o.) — stawki, wyceny, zlecenia, finanse.

## Start dla agenta / developera

1. Przeczytaj `AGENTS.md` i `GROUNDING.md`.
2. Sprawdź `docs/state/CURRENT.md` — bieżący plaster.
3. Uruchom `/plaster` w Cursorze.

## Archiwum dokumentacji projektowej

Pełne materiały planistyczne (60+ plików MD, aneksy, rejestr modułów, audyty):

```
Informacje z claude/
```

Kanoniczne pliki operacyjne żyją w `docs/` tego repozytorium. Nie duplikuj aneksów —
wskaż ścieżkę do archiwum przy potrzebie głębszego kontekstu.

## Lokalnie bez Dockera (Windows, bez wirtualizacji)

```powershell
# 1) dociąga openfga.exe, próbuje Postgres/winget, migracje, opcjonalny seed
powershell -ExecutionPolicy Bypass -File scripts/dev-native.ps1

# jeśli Postgres już jest skonfigurowany:
powershell -ExecutionPolicy Bypass -File scripts/dev-native.ps1 -SkipInstall -Seed
```

Wymaga natywnego **PostgreSQL 16** (instalator EDB / winget — często z UAC).  
OpenFGA: `tools/openfga/openfga.exe` (gitignored, skrypt pobiera).  
Seed: `scripts/dev_seed_local.py`.  
`just dev` nadal stawia **Postgres w Dockerze** — skrypt natywny jest alternatywą, nie zamianą recipe.

## Stan faz

- **0.5–0.15 + B.7:** done (HITL, JWT, hasła+refresh, HTTP extract unit/stub)
- **Następny:** D0 (uczciwość OS) → 0.15 T0 `document_base64` max_length
- Szczegóły: `docs/PLAN-REALIZACJA.md` · dług poza sync: `docs/ops/docs-debt.md`
