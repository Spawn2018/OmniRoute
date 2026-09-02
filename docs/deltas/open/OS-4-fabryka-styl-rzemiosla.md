# OS-4 — styl rzemiosła (slop pada w teście)

**Status:** open  
**Data:** 2026-09-02  
**Oś:** fabryka. **Poza osią Q/S.** Nie startuje zamiast S4.

Skaner `scripts/quality/craft_style.py` w `just craft-style` (`meta-gate`) i w `factory_cycle --start/--close`.

To **nie** jest tożsamość z kodem pisanym przez człowieka. Test nie ocenia merytoryki spedycji ani smaku. Blokuje mechanikę z `no-slop.mdc` / AGENTS, zanim wejdzie na `main`.

| Oracle | Pada gdy | Milczy gdy |
|---|---|---|
| Slop produktu | TODO, `except Exception`, `float()`, echo-komentarz, baner, emoji, `as any`, klasa `*Factory`/`*Manager`, `HTTPException` w `services/` | uzasadniony komentarz *dlaczego*; `frontend/src/lib/utils.ts` (shadcn `cn`) |
| Sufit funkcji | `long_functions` albo `long_function_overflow` rośnie | liczba funkcji >40 linii i suma nadmiaru tylko spada albo stoi |

Pięć istniejących funkcji >40 linii zostaje — ratchet, nie wielki refaktor w tym commicie.

Nie Auto-AGENTS. Nie GROUNDING. Nie kod produktu S4.
