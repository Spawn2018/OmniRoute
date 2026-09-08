from uuid import UUID

from app.domain.errors import InvalidBookingInstruction

_SCOPES = frozenset(
    {"precarriage", "ocean", "oncarriage", "contact_exchange", "none"},
)
_ROLES = frozenset(
    {
        "shipper",
        "consignee",
        "origin_agent",
        "dest_agent",
        "ocean_carrier",
        "omni_customs",
        "client_customs",
    },
)
_STATUSES = frozenset(
    {"suggested", "accepted", "sent", "confirmed", "rejected"},
)
_MAX_REF = 256
_FIXTURE = "fixture://booking-instruction/"
_MANUAL = "tenant:manual"


def require_instruction_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidBookingInstruction("shipment_id musi być UUID")
    return raw


def require_booking_scope_token(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidBookingInstruction("booking_scope musi być tekstem")
    token = raw.strip()
    if token not in _SCOPES:
        raise InvalidBookingInstruction("nieznany zakres bookingu")
    return token


def require_instruction_target_role(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidBookingInstruction("target_role musi być tekstem")
    token = raw.strip()
    if token not in _ROLES:
        raise InvalidBookingInstruction("nieznana rola celu bookingu")
    return token


def require_instruction_status(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidBookingInstruction("status musi być tekstem")
    token = raw.strip()
    if token not in _STATUSES:
        raise InvalidBookingInstruction("nieznany status instrukcji")
    return token


def require_instruction_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidBookingInstruction("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidBookingInstruction("wskazanie zapisu instrukcji")
    if len(token) > _MAX_REF:
        raise InvalidBookingInstruction("wskazanie zapisu instrukcji za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidBookingInstruction("obce wskazanie zapisu instrukcji")
    return token
