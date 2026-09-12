# BC rail_cim_mark (EXP4.2)

HITL katalog znacznika rail UIC/CIM/SMGS per tenant. mark_code + rail_kind
uic|cim|smgs|other + source_ref. Nie rail live filing. Nie scrape.

## Dozwolone zaleznosci
- `app.models.rail_cim_mark`
- `app.repositories.rail_cim_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipment_legs, charges, extraction)
- zapis `shipment_leg` / `charge` / `extraction_draft`
- rail live filing · CIM scrape · kwota
- HTTP
- UPDATE / DELETE wiersza
