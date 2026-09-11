# BC yard_mark (G15)

HITL katalog znacznika yard / waga / EIR per tenant. mark_code + yard_kind
yard_slot|weigh|eir|other + source_ref. Nie live yard. Nie WMS. Nie kg.

## Dozwolone zależności
- pp.models.yard_mark
- pp.repositories.yard_marks
- pp.domain

## Zakaz
- import innych BC services (dock_appointments, containers, charges, extraction)
- zapis dock_appointment / container / charge / extraction_draft
- live yard / WMS / T8 / weigh SQL vs VGM / EIR PDF / PIN
- kwota / marża / float
- HTTP
- UPDATE / DELETE wiersza
