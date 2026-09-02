# OS-3 — test, how-to, delta zanim kod

**Status:** open  
**Data:** 2026-09-02  
**Oś:** fabryka. **Poza osią Q/S.** Nie startuje zamiast S4.

Trzy orakula w `scripts/quality/craft_oracles.py`, wpinane w `craft_close --check` (`just meta-gate`) i `--start plaster`.

| Oracle | Pada gdy | Milczy gdy |
|---|---|---|
| Test z kodem | nowy `services/` lub `api/` `.py` bez `backend/tests/` | jest test w przeglądzie; samo `__init__.py` |
| How-to albo leftover | nowy `catalog-page.tsx` albo `router.post` bez `docs/operator/` i bez `docs-debt.md` | how-to albo linia leftover w tym samym przeglądzie |
| Delta zanim produkt | `backend/app/`, Alembic, `features/`, `routes/` bez delty nie-`OS-*` i bez archiwum w commicie | jest delta produktu w `open/` albo archived w tym commicie |

`/plan-modul` i `/noc` **nie** wymagają delty produktu na starcie (plan ją dopiero tworzy). `/plaster` wymaga.

Nie Auto-AGENTS. Nie GROUNDING. Nie kod produktu S4.
