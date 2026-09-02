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


def require_rfq_party(rfq_party_id: UUID | None, party_id: UUID) -> UUID:
    if rfq_party_id is None:
        raise InvalidCustomerRfq("zapytanie bez kontrahenta — najpierw dopasuj nadawcę")
    if rfq_party_id != party_id:
        raise InvalidCustomerRfq("kontrahent wyceny musi być z zapytania")
    return rfq_party_id
