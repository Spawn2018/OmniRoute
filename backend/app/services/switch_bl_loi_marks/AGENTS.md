# BC switch_bl_loi_mark (EXP3.9)

HITL katalog znacznika switch BL/LOI per tenant. mark_code + instrument_kind
bl|loi|switch|other + source_ref. Nie switch BL live. Nie LOI scrape.

## Dozwolone zaleznosci
- `app.models.switch_bl_loi_mark`
- `app.repositories.switch_bl_loi_marks`
- `app.domain`

## Zakaz
- import innych BC services (ocean_bills, charges, extraction)
- zapis `ocean_bill` / `charge`
- switch BL live · LOI scrape · kwota
- HTTP
- UPDATE / DELETE wiersza
