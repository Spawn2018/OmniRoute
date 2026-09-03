# BC mail_draft (M-57)

Szkic wychodzącego maila obok extractu. Nie czat, nie send, nie drugi rate_line.

## Dozwolone zależności
- `app.models.mail_draft`
- `app.repositories.mail_drafts`
- `app.domain`

## Zakaz
- import innych BC services (extraction, inbound, quotations, operator_decisions)
- zapis `rate_line` / `charge` / `quotation` / `extraction_draft`
- HTTP do Graph / IMAP / SMTP
- liczenie kwot / marży / float
- skład treści przez LLM
