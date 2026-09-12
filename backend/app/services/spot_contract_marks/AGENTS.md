# BC spot_contract_mark (EXP1)

HITL katalog znacznika spot/contract per tenant. mark_code + deal_kind
spot|contract|other + source_ref. Nie FK quotation. Nie cargo_value.

## Dozwolone zależności
- `app.models.spot_contract_mark`
- `app.repositories.spot_contract_marks`
- `app.domain`

## Zakaz
- import innych BC services (quotations, charges, extraction)
- zapis `quotation` / `charge` / `extraction_draft`
- kolumna spot_or_contract / matching SQL / MQC egzekucja
- kwota / marża / float / score
- HTTP
- UPDATE / DELETE wiersza
