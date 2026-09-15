# BC extraction_prompt_mark (AI3.1 leftover)

HITL katalog znacznika promptu ekstrakcji per tenant. mark_code + prompt_kind
extract|system|other + source_ref. Nie wiring LLM. Nie bajty promptu.

## Dozwolone zależności
- `app.models.extraction_prompt_mark`
- `app.repositories.extraction_prompt_marks`
- `app.domain`

## Zakaz
- import innych BC services (extraction, charges, mail_drafts)
- zapis `extraction_draft` / `charge` / `mail_draft`
- Instructor live / wiring LLM / bajty promptu / ciphertext
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
