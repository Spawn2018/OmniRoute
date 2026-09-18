# postal_epo_mark (F11 leftover)

## Fakt
- Tabela `postal_epo_mark`: organization_id, mark_code, epo_kind (`shipment`|`scheme`|`both`|`other`), source_ref.
- Append-only HITL. RLS FORCE. OpenFGA `can_manage_postal_epo_marks`.
- API GET/POST `/postal-epo-marks`. UI `/postal-epo-marks`.

## Nie
- live PP/scheme · e-Doręczenia · SENT XML · kwota
