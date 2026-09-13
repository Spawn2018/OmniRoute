# BC nac_mark (BR4.3)

HITL katalog znacznika NAC / agenta nominowanego per tenant. mark_code + nac_kind
nac|nominated|agent|other + source_ref. Nie live NAC HTTP. Nie FK shipment_stakeholder.

## Dozwolone zależności
- `app.models.nac_mark`
- `app.repositories.nac_marks`
- `app.domain`

## Zakaz
- import innych BC services (shipment_stakeholders, document_dispatch_rules, charges, extraction)
- zapis `shipment_stakeholder` / `document_dispatch_rule` / `charge` / `extraction_draft`
- live NAC HTTP · auto-send dokumentów · kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
