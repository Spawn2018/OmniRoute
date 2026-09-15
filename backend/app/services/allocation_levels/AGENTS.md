# BC allocation_level (AI7.0)

HITL otwarty słownik poziomu alokacji kosztów per tenant. level_code + source_ref.
Nowy poziom = INSERT. Nie CHECK 12. Nie SQL alokacji. Nie druga marża.

## Dozwolone zależności
- `app.models.allocation_level`
- `app.repositories.allocation_levels`
- `app.domain`

## Zakaz
- import innych BC services (allocation_keys, cost_category_marks, charges, extraction)
- zapis `allocation_key` / `cost_category_mark` / `charge` / `extraction_draft`
- CHECK listy 12 poziomów / ENUM / allocation SQL / ABC
- TRUE CONTRIBUTION MARGIN / druga marża / kwota / float
- HTTP
- UPDATE / DELETE wiersza
