# M-57 AI — tablica `extraction_draft` pending (Art. 50)

**Moduł żywy:** M-57 (token UI `ai_copilot`, nie tabela) + M-20 `extraction_draft`  
**Plaster:** **47.0** (plan)  
**Status:** operator **zobaczy** szkice pending jako propozycje AI. Nie tabela czatu. Nie accept.

Delta: [docs/deltas/open/47.0-ai-copilot.md](../deltas/open/47.0-ai-copilot.md).

## 47.0 tablica odczytu na `/ai`

### Zakres

- Ekran `/ai`: `aiProposals` zostawia `status` pending
- Pokazuje `source_ref`; nie `input_text`
- Link do `/extractions`
- Zero nowej tabeli

### Poza 47.0

Tabela czatu · accept z tej trasy · scoring osoby

### HC

- Marża zostaje w `charge`.
- LLM nie liczy kandydatów.
- HITL zostaje na `/extractions`.
- ExtractionService nie importuje rates
