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
just gate    # bramka jakości (patrz PLAN: co jest realne vs stub)
just check   # lint + typy (backend)
just test    # testy
just arch    # import-linter
cd frontend; pnpm dev   # PowerShell: użyj ; nie &&
```

## Stan faz

- **0+A+A.5+B.2–B.4:** done (RLS, OpenFGA, CI green)
- **B.5 (0.5):** Frontend Shell — lokalnie / w toku push
- **B.6 (0.6):** DataTableShell — następny
- **B.7:** branch protection — ograniczenie GitHub Free private (403); szczegóły w `docs/PLAN-REALIZACJA.md`
