# BC allocation_key (AI7.0)

HITL otwarty słownik klucza alokacji kosztów per tenant. key_code + source_ref.
Nowy klucz = INSERT. Nie CHECK 23. Nie SQL alokacji. Nie druga marża.

## Dozwolone zależności
- `app.models.allocation_key`
- `app.repositories.allocation_keys`
- `app.domain`

## Zakaz
- import innych BC services (cost_allocation_marks, charges, extraction)
- zapis `cost_allocation_mark` / `charge` / `extraction_draft`
- CHECK listy 23 kluczy / ENUM / allocation SQL / ABC
- TRUE CONTRIBUTION MARGIN / druga marża / kwota / float
- HTTP
- UPDATE / DELETE wiersza
