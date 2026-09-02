# M-68 obserwowalność — tablica `fetchHealth`

**Moduł żywy:** M-68 (token UI `observability`, nie tabela)  
**Plaster:** **48.0** (plan)  
**Status:** operator **zobaczy** status API. Nie OTel. Nie k6.

Delta: [docs/deltas/open/48.0-observability.md](../deltas/open/48.0-observability.md).

## 48.0 tablica odczytu na `/health`

### Zakres

- Ekran `/health`: `fetchHealth`
- Link do `/`
- Zero nowej tabeli

### Poza 48.0

OTel · k6 · mapa

### HC

- Marża zostaje w `charge`.
- LLM nie liczy.
- HITL zostaje.
- ExtractionService bez zmian
