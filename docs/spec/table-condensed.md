# U-condensed — trzeci tryb gęstości na gridzie stawek

**Leftover żywy:** U-condensed (PLAN § Wave FE, token UI `table_density_condensed`, nie tabela)  
**Plaster:** **53.0** (zamknięty)  
**Status:** operator **widzi** zagęszczone wiersze na `/rate-lines`. Nie globalnie. Nie nowa tabela.

Delta: [docs/deltas/archived/53.0-table-condensed.md](../deltas/archived/53.0-table-condensed.md).

## 53.0 `condensed` tylko na `rate_line`

### Zakres

- `allowCondensed` na DataTableShell
- `/rate-lines` włącza tryb; inne katalogi bez opcji
- Virtualizer 24 px przy condensed
- Zero nowej tabeli i trasy

### Poza 53.0

Condensed na charges · freeze · Base UI

### HC

- Marża zostaje w `charge`.
- LLM nie liczy.
- HITL zostaje.
- Stawki niemutowalne — zmiana gęstości to widok, nie UPDATE kwoty.
