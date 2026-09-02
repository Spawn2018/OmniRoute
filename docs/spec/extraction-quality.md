# M-69 jakość — tablica `unparsed_regions` na szkicu

**Moduł żywy:** M-69 (token UI `extraction_quality`, nie tabela) + M-20 `extraction_draft`  
**Plaster:** **49.0** (plan)  
**Status:** operator **zobaczy** szkice z nierozpoznanymi regionami. Nie tabela QA. Nie scoring.

Delta: [docs/deltas/open/49.0-extraction-quality.md](../deltas/open/49.0-extraction-quality.md).

## 49.0 tablica odczytu na `/quality`

### Zakres

- Ekran `/quality`: `qualityGaps` zostawia wiersze z niepustym `unparsed_regions`
- Pokazuje `source_ref` i regiony; nie `input_text`
- Link do `/extractions` i `/ai`
- Zero nowej tabeli

### Poza 49.0

Tabela QA · scoring `ab_delta_chars` · accept

### HC

- Marża zostaje w `charge`.
- LLM nie ocenia jakości liczbą.
- HITL zostaje na `/extractions`.
- ExtractionService nie importuje rates
