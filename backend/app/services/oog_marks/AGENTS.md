# BC oog_mark (G5)

HITL katalog znacznika OOG per tenant. mark_code + escort_kind oog|lashing|escort|other + source_ref. Nie wymiary. Nie kwota.

## Dozwolone zależności
- `app.models.oog_mark`
- `app.repositories.oog_marks`
- `app.domain`

## Zakaz
- import innych BC services (dangerous_goods, charges, extraction, geography)
- zapis `dangerous_good` / `charge` / `shipment` / `stop`
- wymiary Decimal / lashing_cert / escort party FK / amount / float / kwota
- HTTP
- UPDATE / DELETE wiersza
