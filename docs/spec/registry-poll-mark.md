# registry_poll_mark (EXP7.2)

HITL katalog znacznika poll rejestru per tenant. Nie live CEIDG/KRS/VIES. Nie auto notice.

## Zakres

- Tabela `registry_poll_mark`: organization_id, mark_code, poll_kind (`ceidg`|`krs`|`vies`|`whitelist`|`other`), source_ref, created_at.
- RLS + unique (organization_id, mark_code).
- API GET/POST `/registry-poll-marks`. OpenFGA `can_edit`.
- UI lista + formularz.
- Nie UPDATE/DELETE. Nie FK do party. Nie HTTP rejestrów.

## Poza zakresem

- Live CEIDG / KRS / VIES / biała lista
- auto INSERT operator_notice
- scrape / Selenium
- charge / marża

## Zależności

- M-10 party (klej poza tym plastrem)
