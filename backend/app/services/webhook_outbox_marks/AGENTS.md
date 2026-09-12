# BC webhook_outbox_mark (EXP2.23)

HITL katalog znacznika webhook outbox per tenant. mark_code + outbox_kind
webhook|retry|dead|other + source_ref. Nie live dispatch. Nie Temporal.
Obok outbox_event — tu znacznik trybu, nie zdarzenie między BC.

## Dozwolone zaleznosci
- `app.models.webhook_outbox_mark`
- `app.repositories.webhook_outbox_marks`
- `app.domain`

## Zakaz
- import innych BC services (outbox_events, charges, extraction)
- zapis `outbox_event` / `charge` / `extraction_draft`
- live webhook HTTP · Temporal · Hatchet · JSON payload
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
