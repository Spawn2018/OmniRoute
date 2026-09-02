from uuid import UUID

from app.domain.errors import InvalidCustomerRfq
from app.domain.inbound_message import require_inbound_source_ref

_DRAFT = "draft"


def customer_rfq_draft_status() -> str:
    return _DRAFT


def require_rfq_source_ref(raw: object) -> str:
    return require_inbound_source_ref(raw)


def require_inbound_message_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidCustomerRfq("inbound_message_id musi być UUID")
    return raw
