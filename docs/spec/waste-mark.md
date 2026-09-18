# waste_mark (C6 leftover)

## Zakres

- Tabela `waste_mark`: organization_id, mark_code, waste_kind (`bdo`|`kpo`|`wsr`|`other`), source_ref.
- Append-only HITL. RLS FORCE. OpenFGA `can_manage_waste_marks`.

## Poza zakresem

- MOS live / BDO HTTP / `shipment.is_waste` / kwota
