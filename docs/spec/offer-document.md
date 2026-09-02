# M-26 dokument oferty — podgląd faktów `quotation`

**Moduł żywy:** M-26 (token UI `offer_document`, nie tabela) + ekran M-21 `quotation`  
**Plaster:** **19.0** (plan)  
**Status:** plan — wycena **pokazuje** swoje pola jako dokument. Nie PDF. Nie `@media print` (U-print = Fala 5/6).

Delta: [docs/deltas/open/19.0-offer-document.md](../deltas/open/19.0-offer-document.md).

## 19.0 podgląd dokumentu oferty

### Zakres

- Na `/quotations`: panel „Dokument oferty” — wybór wiersza, `<dl>` z kodem, kwotą (`<Money/>`), POL/POD, kontrahentem, `source_ref`
- Zero nowej tabeli. Zero blob/PDF. Zero `window.print`

### Poza 19.0

PDF · szablon FV/B/L (`U-print`) · letterhead z `organization_setting` · LLM piszący treść · mutacja kwoty

### HC

- Kwota zostaje ze `rate_line` (SQL). Dokument nic nie liczy.
- LLM nie liczy. `charge` zostaje prawdą o marży.
- ExtractionService nie importuje quotations
