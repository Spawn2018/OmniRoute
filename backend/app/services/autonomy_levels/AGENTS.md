# BC autonomy_level (AI1.4 leftover)

HITL otwarty słownik poziomu autonomii per tenant. level_code + source_ref.
Nowy poziom = INSERT. Nie CHECK 0-5. Nie FK party. Nie silnik L3+.

## Dozwolone zależności
- `app.models.autonomy_level`
- `app.repositories.autonomy_levels`
- `app.domain`

## Zakaz
- import innych BC services (parties, suggestion_kinds, twin_kinds, charges, extraction)
- zapis `party` / `app_user` / `charge` / `extraction_draft`
- CHECK listy poziomów B.4 / ENUM / FK klienta
- silnik L3+ / kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
