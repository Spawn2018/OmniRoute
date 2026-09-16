from datetime import date
from decimal import Decimal
from typing import NamedTuple
from uuid import UUID

from app.domain.channel_quote import (
    normalize_quote_amount,
    normalize_quote_currency,
    normalize_transit_days,
)
from app.domain.errors import InvalidCarrierInquiry

_DRAFT = "draft"
_ANSWERED = "answered"
_MANUAL = "tenant:manual"
_STATUSES = frozenset({"draft", "queued", "sent", "answered", "declined"})
_ANSWERABLE = frozenset({"draft", "queued", "sent"})
_GROUP_BY = frozenset({"party", "country", "status", "thread"})
_GROUP_DEFAULT = "party"


def carrier_inquiry_draft_status() -> str:
    return _DRAFT


def carrier_inquiry_manual_source() -> str:
    return _MANUAL


class InquiryMemberRank(NamedTuple):
    network_member_id: UUID
    answered_count: int


def default_buy_desk_group_by() -> str:
    return _GROUP_DEFAULT


def require_buy_desk_group_by(raw: object) -> str:
    if raw is None:
        return _GROUP_DEFAULT
    if type(raw) is not str:
        raise InvalidCarrierInquiry("group_by musi być tekstem")
    token = raw.strip()
    if token == "":
        return _GROUP_DEFAULT
    if token not in _GROUP_BY:
        raise InvalidCarrierInquiry("group_by spoza allowlisty")
    return token


def buy_desk_group_key(
    *,
    group_by: str,
    status: str,
    party_id: UUID | None,
    country_code: str | None,
    origin_port_id: UUID | None,
    destination_port_id: UUID | None,
) -> str:
    token = require_buy_desk_group_by(group_by)
    if token == "status":
        return status
    if token == "country":
        if country_code is None or country_code == "":
            return "—"
        return country_code
    if token == "thread":
        origin = "—" if origin_port_id is None else str(origin_port_id)
        dest = "—" if destination_port_id is None else str(destination_port_id)
        return f"{origin}|{dest}"
    if party_id is None:
        return "—"
    return str(party_id)


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


def require_no_reply_after(raw: object) -> date | None:
    if raw is None:
        return None
    if type(raw) is date:
        return raw
    if type(raw) is not str:
        raise InvalidCarrierInquiry("no_reply_after: data kalendarzowa")
    token = raw.strip()
    if token == "":
        return None
    try:
        return date.fromisoformat(token)
    except ValueError as exc:
        raise InvalidCarrierInquiry("no_reply_after: data kalendarzowa") from exc


def require_silent_filter(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidCarrierInquiry("silent: overdue albo pusto")
    token = raw.strip()
    if token == "":
        return None
    if token != "overdue":
        raise InvalidCarrierInquiry("silent: overdue albo pusto")
    return token


def require_member_batch(raw: object) -> list[UUID]:
    if type(raw) is not list or raw == []:
        raise InvalidCarrierInquiry("batch wymaga listy członków")
    return [require_network_member_id(item) for item in raw]


def require_answerable_status(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCarrierInquiry("status zapytania musi być tekstem")
    token = raw.strip()
    if token not in _ANSWERABLE:
        raise InvalidCarrierInquiry("status zapytania nie pozwala na answered")
    return token


def carrier_inquiry_answered_status() -> str:
    return _ANSWERED


def require_answered_quote(
    *,
    status: str,
    quoted_amount: object,
    quoted_currency: object,
    quoted_transit_days: object,
) -> tuple[Decimal | None, str | None, int | None]:
    if status != _ANSWERED:
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
