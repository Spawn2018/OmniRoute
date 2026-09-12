# BC phyto_ata_mark (EXP3.8)

HITL katalog znacznika phyto/ATA per tenant. mark_code + permit_kind
phyto|ata|plant|other + source_ref. Nie phyto live. Nie ATA scrape.

## Dozwolone zaleznosci
- `app.models.phyto_ata_mark`
- `app.repositories.phyto_ata_marks`
- `app.domain`

## Zakaz
- import innych BC services (commodity_codes, charges, extraction)
- zapis `commodity_code` / `charge`
- phyto live · ATA scrape · kwota
- HTTP
- UPDATE / DELETE wiersza
