# yard_mark (G15)

HITL katalog znacznika yard / waga / EIR per tenant. Nie live yard. Nie WMS. Nie waga SQL.

## Zakres

- Tabela `yard_mark`: organization_id, mark_code, yard_kind (`yard_slot`|`weigh`|`eir`|`other`), source_ref, created_at.
- RLS + unique (organization_id, mark_code).
- API GET/POST `/yard-marks`. OpenFGA `can_edit`.
- UI lista + formularz.
- Nie UPDATE/DELETE. Nie FK do dock_appointment/container. Nie kg. Nie EIR PDF.

## Poza zakresem

- Live yard / WMS / kamera / T8 slot optimizer
- weigh_in/out vs VGM SQL / float kg
- EIR bajty / PIN terminala
- charge / marża

## Zależności

- D3 dock_appointment, T3 container (klej poza tym plastrem)
