# M-26 dokument oferty — fakty `quotation` + numer

**Moduł żywy:** M-26 (token UI `offer_document`, nie tabela) + ekran M-21 `quotation`  
**Plaster:** **19.0** (podgląd) · **72.0** (numer + druk 57.0)  
**Status:** operator nadaje `document_number` z prefiksu M-03 i drukuje arkuszem 57.0. Nie PDF. Nie send.

Delta: [docs/deltas/archived/72.0-offer-document-number.md](../deltas/archived/72.0-offer-document-number.md). Fundament: [19.0](../deltas/archived/19.0-offer-document.md).

## 72.0 numer na dokumencie

### Zakres

- `quotation.document_number` nullable, unikat per tenant
- `POST /quotations/{id}/document-number` — kolejny numer z SQL (`MAX` ogona + prefiks)
- `GET /quotations/document-layout` — prefiks i token `plain`/`letter`
- Panel: „Nadaj numer”, „Drukuj” (`window.print`), `data-print-template`

### Poza 72.0

PDF · letterhead blob · send / Graph · nowy silnik stawek · F9.1

### HC

- Kwota zostaje ze `rate_line` (SQL). Numer nic nie liczy w Pythonie poza złożeniem prefiksu.
- Serwis wyceny nie importuje `organization_settings`. API składa prefiks.
- LLM nie liczy. `charge` zostaje prawdą o marży.

## 19.0 podgląd dokumentu oferty

### Zakres

- Na `/quotations`: panel „Dokument oferty” — wybór wiersza, `<dl>` z kodem, kwotą (`<Money/>`), POL/POD, kontrahentem, `source_ref`
- Zero nowej tabeli. Zero blob/PDF.

### HC

- Kwota zostaje ze `rate_line` (SQL). Dokument nic nie liczy.
- ExtractionService nie importuje quotations
