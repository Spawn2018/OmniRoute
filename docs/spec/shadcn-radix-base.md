# U-primitives-json — pin Radix w `components.json`

**Leftover żywy:** U-primitives-json (PLAN § Wave FE, token `shadcn_radix_base`, nie tabela)  
**Plaster:** **54.0** (plan)  
**Status:** operator **nie** zobaczy ekranu — CLI `shadcn add` ma brać Radix. Nie Base UI. Nie nowa tabela.

Delta: [docs/deltas/open/54.0-shadcn-radix-base.md](../deltas/open/54.0-shadcn-radix-base.md).

## 54.0 plik `frontend/components.json`

### Zakres

- `"base": "radix"`, `rsc: false`, aliasy `@/`, CSS `src/index.css`
- Test pinu; zero `@base-ui` w zależnościach
- Zero nowej tabeli i trasy

### Poza 54.0

Nowe komponenty z CLI · i18n · Playwright

### HC

- Marża zostaje w `charge`.
- LLM nie liczy.
- HITL zostaje.
- Jeden zestaw primitywów (Radix).
