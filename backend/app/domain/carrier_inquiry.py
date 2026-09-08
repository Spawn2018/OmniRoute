from decimal import Decimal
from uuid import UUID

from app.domain.channel_quote import (
    normalize_quote_amount,
    normalize_quote_currency,
    normalize_transit_days,
)
from app.domain.errors import InvalidCarrierInquiry

_DRAFT = "draft"
_MANUAL = "tenant:manual"
_STATUSES = frozenset({"draft", "queued", "sent", "answered", "declined"})


def carrier_inquiry_draft_status() -> str:
    return _DRAFT


def carrier_inquiry_manual_source() -> str:
    return _MANUAL


def require_network_member_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidCarrierInquiry("network_member_id musi być UUID")
    return raw


def require_inquiry_status(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCarrierInquiry("status zapytania musi być tekstem")
    token = raw.strip()
    if token not in _STATUSES:
        raise InvalidCarrierInquiry("status zapytania spoza allowlisty")
    return token


def require_inquiry_port_id(raw: object, *, field: str) -> UUID | None:
    if raw is None:
        return None
    if type(raw) is not UUID:
        raise InvalidCarrierInquiry(f"{field} musi być UUID")
    return raw


def require_member_batch(raw: object) -> list[UUID]:
    if type(raw) is not list or raw == []:
        raise InvalidCarrierInquiry("batch wymaga listy członków")
    return [require_network_member_id(item) for item in raw]


def require_answered_quote(
    *,
    status: str,
    quoted_amount: object,
    quoted_currency: object,
    quoted_transit_days: object,
) -> tuple[Decimal | None, str | None, int | None]:
    if status != "answered":
        if quoted_amount is not None or quoted_currency is not None:
            raise InvalidCarrierInquiry("kwota odpowiedzi tylko przy answered")
        if quoted_transit_days is not None:
            raise InvalidCarrierInquiry("TT odpowiedzi tylko przy answered")
        return None, None, None
    if quoted_amount is None or quoted_currency is None:
        raise InvalidCarrierInquiry("answered wymaga kwoty i waluty")
    return (
        normalize_quote_amount(quoted_amount),
        normalize_quote_currency(quoted_currency),
        normalize_transit_days(quoted_transit_days),
    )
