# U-print — arkusz druku B/L / FV / list

**Leftover żywy:** U-print (PLAN § Wave FE, token `print_sheet`, nie tabela)  
**Plaster:** **57.0** (zamknięty)  
**Status:** operator **drukuje** z przeglądarki: sidebar i pasek akcji znikają. Nie PDF. Nie nowa tabela.

Delta: [docs/deltas/archived/57.0-print-sheet.md](../deltas/archived/57.0-print-sheet.md).

## 57.0 `@media print` w `index.css`

### Zakres

- `@media print` chowa `aside`, `header`, przycisk ⌘K
- Zostają panele `data-offer-document`, `data-sales-invoice`, `data-shipment-document`
- Test pinu arkusza; zero `jspdf` / `pdf-lib`
- Zero nowej tabeli i trasy

### Poza 57.0

Generowanie PDF · HBL jako tabela · letterhead · KSeF

### HC

- Marża zostaje w `charge`.
- LLM nie liczy.
- HITL zostaje.
- Kwota na druku zostaje `<Money/>` string, nie float.
