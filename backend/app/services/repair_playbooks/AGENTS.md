# BC repair_playbook (CI8)

HITL katalog playbooka naprawy per tenant. playbook_code + stance_kind contain|reroute|claim|other + source_ref. Nie auto-send. Nie mail_draft.

## Dozwolone zależności
- `app.models.repair_playbook`
- `app.repositories.repair_playbooks`
- `app.domain`

## Zakaz
- import innych BC services (charges, mail_drafts, remediation_options, extraction)
- zapis `charge` / `mail_draft` / `remediation_option`
- auto-send S11 / kwota / marża / float / mail_body
- HTTP
- UPDATE / DELETE wiersza
