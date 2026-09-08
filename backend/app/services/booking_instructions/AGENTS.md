# BC booking_instruction (I4)

Instrukcja bookingu na zleceniu: scope + rola + status. Nie HTTP armatora. Nie mail.

## Dozwolone zależności
- `app.models.booking_instruction`
- `app.repositories.booking_instructions`
- `app.domain`

## Zakaz
- import innych BC services (shipments, incoterm_responsibilities, mail_drafts, charges)
- zapis `shipment` / `incoterm_responsibility` / `mail_draft` / `charge`
- kwoty / marża / float
- HTTP / S21 / Selenium
