from uuid import UUID

from app.domain.charge_code import normalize_aliases
from app.domain.errors import IncompleteQuotationSnapshot, InvalidQuotationBatch

_BATCH_CHARGE_CODE_LIMIT = 20


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


def require_batch_charge_codes(raw: list[str]) -> list[str]:
    tokens = normalize_aliases(raw)
    if len(tokens) == 0:
        raise InvalidQuotationBatch("wycena wsadowa wymaga co najmniej jednego kodu")
    if len(tokens) > _BATCH_CHARGE_CODE_LIMIT:
        raise InvalidQuotationBatch("wycena wsadowa: max 20 kodów")
    return tokens

