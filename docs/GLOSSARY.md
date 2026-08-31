# Słownik domenowy PL / EN

| PL | EN (kod) | Uwagi |
|---|---|---|
| stawka | rate_line | niemutowalna, source_ref |
| opłata / charge | charge / shipment_charge | jedyne miejsce prawdy o marży |
| wycena | quotation | |
| luka wyceny | quotation_gap | brakująca dopłata |
| zlecenie | shipment | handlowe |
| odcinek | shipment_leg | operacyjne |
| tenant | organization | organization_id wszędzie |
| pochodzenie | source_ref | obowiązkowe |
| szkic ekstrakcji | extraction_draft | HITL przed zapisem domeny |
| region nierozpoznany | unparsed_region | zawsze w payloadzie ekstrakcji |
| kurs NBP | nbp_rate | D-1 roboczy |
| narzut | markup | kaskada — Python mały zbiór (DECISIONS) |

Pełny słownik: kompilacja z `Informacje z claude/OmniRoute-dokumentacja/docs/` w Fazie B.
