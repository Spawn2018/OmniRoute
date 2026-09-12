# BC e_cmr_mark (EXP2.18)

HITL katalog znacznika e-CMR/eFTI per tenant. mark_code + cmr_kind
ecmr|efti|paper|other + source_ref. Nie filer live. Nie e-CMR HTTP.
Obok `filing_scheme_mark` (G12) — tu dokument przewozowy, nie schemat ICS2/CBAM.

## Dozwolone zależności
- `app.models.e_cmr_mark`
- `app.repositories.e_cmr_marks`
- `app.domain`

## Zakaz
- import innych BC services (filing_scheme_marks, shipments, charges, extraction)
- zapis `filing_scheme_mark` / `shipment` / `charge` / `extraction_draft`
- e-CMR live · eFTI filer · paper PDF bytes
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
