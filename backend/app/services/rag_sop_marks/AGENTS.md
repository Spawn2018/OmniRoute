# BC rag_sop_mark (EXP4.18)

HITL katalog znacznika zakresu RAG per tenant. mark_code + scope_kind
sop|adr|mail|other + source_ref. Nie pgvector. Nie wycena.

## Dozwolone zależności
- `app.models.rag_sop_mark`
- `app.repositories.rag_sop_marks`
- `app.domain`

## Zakaz
- import innych BC services (customer_sops, charges, extraction, mail_drafts)
- zapis `customer_sop` / `charge` / `extraction_draft` / `mail_draft`
- pgvector / embedding / RAG na wycenie / kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
