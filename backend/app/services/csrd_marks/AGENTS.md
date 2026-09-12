# BC csrd_mark (EXP3.14)

HITL katalog znacznika raportu CSRD per tenant. mark_code + report_kind
csrd|esrs|assurance|other + source_ref. Nie kg. Nie live filing. Nie marza.

## Dozwolone zaleznosci
- `app.models.csrd_mark`
- `app.repositories.csrd_marks`
- `app.domain`

## Zakaz
- import innych BC services (carbon_methods, charges, extraction)
- zapis `carbon_method` / `charge` / `extraction_draft`
- kg / tCO2e / CSRD live filing / kwota
- HTTP
- UPDATE / DELETE wiersza
