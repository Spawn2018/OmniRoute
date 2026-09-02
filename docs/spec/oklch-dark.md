# U-oklch-dark — tokeny OKLCH i motyw `.dark`

**Leftover żywy:** U-oklch-dark (PLAN § Wave FE, nie tabela)  
**Plaster:** **51.0** (zamknięty)  
**Status:** operator **widzi** paletę OKLCH i motyw ciemny z OS. Nie tabela. Nie nowa trasa.

Delta: [docs/deltas/archived/51.0-oklch-dark.md](../deltas/archived/51.0-oklch-dark.md).

## 51.0 arkusz `index.css`

### Zakres

- Kolory `:root` jako `oklch()` zamiast hex na parach tło/tekst
- Blok `.dark` z odwróconym tłem/tekstem
- `main.tsx` dodaje `.dark` gdy `prefers-color-scheme: dark`
- Test w `a11y.test.ts`
- Zero nowej tabeli i trasy

### Poza 51.0

Money align · condensed · Playwright · print

### HC

- Marża zostaje w `charge`.
- LLM nie liczy kwot.
- HITL zostaje.
- Paleta zostaje w CSS, nie w bazie.
