# M-39 EDI — komunikat na zleceniu

**Moduł żywy:** M-39 (tabela `edi_message`)  
**Plaster:** **95.0** (zamknięty) · fundament odczytu **32.0**  
**Status:** operator **zapisuje** komunikat na zleceniu z kontrahentem. Nie parser. Nie live HTTP.

Delta: [docs/deltas/archived/95.0-edi-message.md](../deltas/archived/95.0-edi-message.md).

## 95.0 tabela na `/edi`

### Zakres

- Tabela `edi_message` per tenant, FK do `shipment`
- Ekran `/edi`: lista wierszy + „Zapisz komunikat”
- Zero parsera. Zero bajtów. Zero live HTTP

### Poza 95.0

Parser · live HTTP · payload · S34 faktura

### HC

- Marża zostaje w `charge`.
- LLM nie składa komunikatu.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje EDI / quotations / shipment
