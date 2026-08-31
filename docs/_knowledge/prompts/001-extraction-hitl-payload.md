# Ekstrakcja HITL — kontrakt payloadu

**Kiedy:** M-20 / plastry 0.7+

## Zasady

1. Model zwraca Intent (`ExtractionPayload`), nigdy nie zapisuje do DB.
2. `source_ref` + `unparsed_regions` obowiązkowe (HC-03).
3. Kwoty tylko jako tekst (`amount_text`) — kod liczy Decimal.
4. Accept HITL nie tworzy `rate_line` do czasu osobnego serwisu (HC-04).

## Referencja kodu

`backend/app/ai_transforms/extraction/schemas.py`
