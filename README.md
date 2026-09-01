# OmniRoute

Wielodostępna platforma spedycyjna (LOGMAR Sp. z o.o.) — stawki, wyceny, zlecenia, finanse.

## Start dla agenta / developera

1. Przeczytaj `AGENTS.md` i `GROUNDING.md`.
2. Sprawdź `docs/state/CURRENT.md` — bieżący plaster.
3. Komenda z sekcji **Stan faz** (generowana z `docs/state/CURRENT.md`).

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

<!-- os-status:start -->
- **Ostatni plaster:** **8.0** M-11 `resolve_email` (zarchiwizowany)
- **Etap:** Plan
- **Następny:** M-12 Sieci i stowarzyszenia (`/plan-modul`). Nie Fala 8. Nie zgaduj zakresu.
- **Komenda teraz:** `/plan-modul` (z `docs/state/CURRENT.md`; nie zgaduj `/plaster` przy Etap Plan)
- **Jedyny plan:** `docs/PLAN-REALIZACJA.md` · `docs/state/CURRENT.md`
<!-- os-status:end -->
