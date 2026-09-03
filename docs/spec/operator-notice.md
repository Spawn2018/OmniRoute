# M-34 powiadomienia — inbox + tablica istniejącej pracy

**Moduł żywy:** M-34 (`operator_notice` tabela + ekran `/notifications`)  
**Plaster:** **27.0** tablica odczytu · **75.0** tabela · **123.0** filtr 27.0 (plan)  
**Status:** operator zapisuje unread i oznacza read. Tablica HITL/wycen pending ma filtr rodzaju. Nie send.

Delta: [27.0](../deltas/archived/27.0-operator-notice.md) · [75.0](../deltas/archived/75.0-operator-notice-table.md) · [123.0](../deltas/open/123.0-notice-pending-filter.md).

## 27.0 tablica odczytu na `/notifications`

### Zakres

- Ekran `/notifications`: lista `extraction_draft` pending + wyceny z `party_id` (22.0)
- Link do `/extractions` i `/quotations`. Zero accept/reject tutaj
- Etykieta Art. 50 przy szkicach AI

### Poza 27.0

Tabela (75.0) · outbox · Temporal · mail transakcyjny · LLM

## 75.0 tabela inbox

### Zakres

- Tabela `operator_notice` per tenant: `kind=manual`, `unread`/`read`, `body`, `source_ref`
- `GET/POST /operator-notices`, `POST /{id}/read` (idempotentny)
- OpenFGA `can_manage_operator_notices`
- UI: zapis na `/notifications` obok tablicy 27.0

### Poza 75.0

Auto-INSERT z HITL/wyceny · send · outbox · S13 draft maila

## 123.0 filtr tablicy 27.0

### Zakres

- Filtr rodzaju na tablicy pending: wszystkie / HITL / wyceny
- Tabela inbox nie jest źródłem tych wierszy

### Poza 123.0

Auto-INSERT · send

## HC

- HITL accept zostaje na kolejce ekstrakcji
- LLM nie liczy i nie pisze treści
- `charge` zostaje prawdą o marży
- ExtractionService nie importuje quotations
- Serwis inbox nie importuje quotations / extraction / inbound
