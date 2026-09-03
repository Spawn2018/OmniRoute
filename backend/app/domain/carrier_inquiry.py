from uuid import UUID

from app.domain.errors import InvalidCarrierInquiry

_DRAFT = "draft"
_MANUAL = "tenant:manual"


def carrier_inquiry_draft_status() -> str:
    return _DRAFT


def carrier_inquiry_manual_source() -> str:
    return _MANUAL


def require_network_member_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidCarrierInquiry("network_member_id musi być UUID")
    return raw
