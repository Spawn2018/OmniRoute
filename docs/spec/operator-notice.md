# M-34 powiadomienia — tablica istniejącej pracy operatora

**Moduł żywy:** M-34 (token UI `operator_notice`, nie tabela) + ekrany M-20 HITL i M-21 `quotation`  
**Plaster:** **27.0** (zamknięty)  
**Status:** operator **widzi** szkice do recenzji i wyceny oczekujące na akceptację. Nie nowa tabela. Nie wysyłka.

Delta: [docs/deltas/archived/27.0-operator-notice.md](../deltas/archived/27.0-operator-notice.md).

## 27.0 tablica odczytu na `/notifications`

### Zakres

- Ekran `/notifications`: lista `extraction_draft` o statusie pending + wyceny z `party_id` (22.0)
- Link do `/extractions` i `/quotations`. Zero accept/reject tutaj
- Etykieta Art. 50 przy szkicach AI
- Zero nowej tabeli. Zero push. Zero SMTP

### Poza 27.0

Tabela `notification` · outbox · Temporal · mail transakcyjny · LLM

### HC

- HITL accept zostaje na kolejce ekstrakcji.
- LLM nie liczy i nie pisze treści.
- `charge` zostaje prawdą o marży.
- ExtractionService nie importuje quotations
