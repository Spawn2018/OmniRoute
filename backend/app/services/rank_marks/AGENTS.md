# BC rank_mark (W5)

HITL katalog osi rankingu zakupu per tenant. rank_kind. Nie auto-award. Nie N szkiców z Top N.

## Dozwolone zależności
- `app.models.rank_mark`
- `app.repositories.rank_marks`
- `app.domain`

## Zakaz
- import innych BC services (networks, mail_drafts, charges, extraction)
- zapis `network_member` / `mail_draft` / `charge` / `carrier_inquiry`
- auto-award / ranking SQL / kwota / marża / float
- HTTP / N szkiców
