# BC label_parking_mark (EXP4.12)

HITL katalog znacznika LABEL parking per tenant. mark_code + parking_kind
secure|labeled|other + source_ref. Nie parking live API. Nie mapa.

## Dozwolone zaleznosci
- `app.models.label_parking_mark`
- `app.repositories.label_parking_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, charges, extraction)
- zapis `trip` / `charge` / `extraction_draft`
- parking live API · mapa parkingow · GPS · kwota
- HTTP
- UPDATE / DELETE wiersza
