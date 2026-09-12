# BC role_view_mark (EXP4.17)

HITL katalog znacznika widoku roli per tenant. mark_code + view_kind
groupage|ftl|ocean|other + source_ref. Nie board T6. Nie mapa.

## Dozwolone zależności
- `app.models.role_view_mark`
- `app.repositories.role_view_marks`
- `app.domain`

## Zakaz
- import innych BC services (trips, charges, extraction, table_views)
- zapis `table_view` / `charge` / `extraction_draft`
- board T6 live · trzy produkty UI · mapa · kwota
- HTTP
- UPDATE / DELETE wiersza
