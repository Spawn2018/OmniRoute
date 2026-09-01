from uuid import UUID

from app.domain.errors import IncompleteQuotationSnapshot


def require_lane_party_snapshot(
    origin_port_id: UUID | None,
    destination_port_id: UUID | None,
    party_id: UUID | None,
) -> tuple[UUID, UUID, UUID]:
    if origin_port_id is None:
        raise IncompleteQuotationSnapshot("wycena wymaga portu załadunku (POL)")
    if destination_port_id is None:
        raise IncompleteQuotationSnapshot("wycena wymaga portu wyładunku (POD)")
    if party_id is None:
        raise IncompleteQuotationSnapshot("wycena wymaga kontrahenta")
    return origin_port_id, destination_port_id, party_id
