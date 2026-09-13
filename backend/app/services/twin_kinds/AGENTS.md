# BC twin_kind (AI1.4 leftover)

HITL otwarty słownik rodzaju bliźniaka per tenant. kind_code + source_ref.
Nowy rodzaj = INSERT. Nie CHECK. Nie twin_mark. Nie fizyka.

## Dozwolone zależności
- `app.models.twin_kind`
- `app.repositories.twin_kinds`
- `app.domain`

## Zakaz
- import innych BC services (twin_marks, suggestion_kinds, charges, extraction)
- zapis `twin_mark` / `suggestion_kind` / `charge` / `extraction_draft`
- CHECK listy 8 rodzajów / ENUM / FK z twin_mark
- fizyka / circle_sim / kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
