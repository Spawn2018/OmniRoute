from typing import NamedTuple
from uuid import UUID

from app.domain.errors import (
    AcceptRequiresChannelQuote,
    ExtractionCandidatesNotEditable,
    InvalidExtractionDraft,
    InvalidTenderRfpIntake,
)
from app.domain.tender_rfp_intake import require_board_id, require_intake_code

_RATE = "rate_line"
_QUOTE = "carrier_quote"
_RFP = "tender_rfp"
_KINDS = frozenset({_RATE, _QUOTE, _RFP})


def extraction_rate_kind() -> str:
    return _RATE


def extraction_carrier_quote_kind() -> str:
    return _QUOTE


def extraction_tender_rfp_kind() -> str:
    return _RFP


def require_rate_candidates_editable(draft_kind: object) -> None:
    if draft_kind != _RATE:
        raise ExtractionCandidatesNotEditable("edycja kandydatów tylko dla szkicu rate_line")


def require_extraction_draft_kind(raw: object) -> str:
    if raw is None:
        return _RATE
    if type(raw) is not str:
        raise InvalidExtractionDraft("draft_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidExtractionDraft("draft_kind spoza allowlisty")
    return token


class CarrierQuoteDraft(NamedTuple):
    party_id: UUID
    origin_port_id: UUID
    destination_port_id: UUID
    quote_date: str
    amount: str
    currency: str
    transit_days: int | None


def _as_uuid(raw: object, field: str) -> UUID:
    if type(raw) is UUID:
        return raw
    if type(raw) is not str or raw.strip() == "":
        raise AcceptRequiresChannelQuote(f"{field} jest obowiązkowy")
    try:
        return UUID(raw.strip())
    except ValueError as exc:
        raise AcceptRequiresChannelQuote(f"{field} musi być UUID") from exc


def _as_text(raw: object, field: str) -> str:
    if type(raw) is not str or raw.strip() == "":
        raise AcceptRequiresChannelQuote(f"{field} jest obowiązkowy")
    return raw.strip()


def require_carrier_quote_payload(raw: object) -> CarrierQuoteDraft:
    if type(raw) is not dict:
        raise AcceptRequiresChannelQuote("payload oferty jest obowiązkowy")
    days = raw.get("transit_days")
    if days is not None and (isinstance(days, bool) or type(days) is not int):
        raise AcceptRequiresChannelQuote("transit_days musi być liczbą całkowitą")
    return CarrierQuoteDraft(
        party_id=_as_uuid(raw.get("party_id"), "party_id"),
        origin_port_id=_as_uuid(raw.get("origin_port_id"), "origin_port_id"),
        destination_port_id=_as_uuid(raw.get("destination_port_id"), "destination_port_id"),
        quote_date=_as_text(raw.get("quote_date"), "quote_date"),
        amount=_as_text(raw.get("amount"), "amount"),
        currency=_as_text(raw.get("currency"), "currency"),
        transit_days=days,
    )


class TenderRfpDraft(NamedTuple):
    tender_id: UUID
    intake_code: str


def require_tender_rfp_payload(raw: object) -> TenderRfpDraft:
    if type(raw) is not dict:
        raise InvalidTenderRfpIntake("przyjęcie: payload obowiązkowy")
    board = raw.get("tender_id")
    if type(board) is str:
        try:
            board = UUID(board.strip())
        except ValueError as exc:
            raise InvalidTenderRfpIntake("tender_id musi być UUID") from exc
    return TenderRfpDraft(
        tender_id=require_board_id(board),
        intake_code=require_intake_code(raw.get("intake_code")),
    )
