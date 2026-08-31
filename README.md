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

## Komendy

```bash
just gate    # pełna bramka jakości
just check   # lint + typy
just test    # testy
just arch    # import-linter
```

## Faza bootstrap

- **Faza 0 (current):** GitHub — repo, git, CI skeleton, branch protection, MCP
- **Faza A (next):** OS Cursor — rules, skills, hooks, docs skeleton, `just gate`
- **Faza B:** Szkielet FastAPI + Vite, RLS plaster 0.3, OpenFGA
