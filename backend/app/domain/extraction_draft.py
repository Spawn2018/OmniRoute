from collections.abc import Sequence
from decimal import Decimal, InvalidOperation
from typing import NamedTuple
from uuid import UUID

from app.domain.errors import (
    AcceptRequiresChannelQuote,
    BulkAcceptConfidenceBelow,
    ExtractionCandidatesNotEditable,
    InvalidExtractionDraft,
    InvalidTenderRfpIntake,
)
from app.domain.tender_rfp_intake import require_board_id, require_intake_code

_RATE = "rate_line"
_QUOTE = "carrier_quote"
_RFP = "tender_rfp"
_KINDS = frozenset({_RATE, _QUOTE, _RFP})
_PATH_TEXT = "text"
_PATH_IMAGE = "image"
_PATHS = frozenset({_PATH_TEXT, _PATH_IMAGE})
_BULK_MIN = Decimal("0.70")
_OK_BANDS = frozenset({"green", "yellow", "high"})
_BAD_BANDS = frozenset({"orange", "hold", "low", "poor"})


def extraction_rate_kind() -> str:
    return _RATE


def extraction_carrier_quote_kind() -> str:
    return _QUOTE


def extraction_tender_rfp_kind() -> str:
    return _RFP


def next_extraction_revision(raw: object) -> int:
    if type(raw) is not int or raw < 0:
        return 1
    return raw + 1


def append_extraction_history(
    history: object,
    *,
    revision: object,
    candidates: object,
) -> list[dict[str, object]]:
    """Snapshot przed PATCH — JSONB, nie tabela (448.0 REJECTED)."""
    entries: list[dict[str, object]] = []
    if type(history) is list:
        for row in history:
            if type(row) is dict:
                entries.append(dict(row))
    prior_revision = revision if type(revision) is int and revision >= 0 else 0
    prior_candidates = list(candidates) if type(candidates) is list else []
    entries.append({"revision": prior_revision, "candidates": prior_candidates})
    return entries


def require_candidate_indexes(raw: object, size: int) -> list[int] | None:
    """None = wszyscy. Lista 0-based, unikalna, w zakresie."""
    if raw is None:
        return None
    if type(raw) is not list:
        raise InvalidExtractionDraft("candidate_indexes musi być listą")
    if len(raw) == 0:
        raise InvalidExtractionDraft("candidate_indexes nie może być puste")
    seen: set[int] = set()
    ordered: list[int] = []
    for entry in raw:
        if type(entry) is not int or isinstance(entry, bool):
            raise InvalidExtractionDraft("indeks kandydata musi być liczbą całkowitą")
        if entry < 0 or entry >= size:
            raise InvalidExtractionDraft("indeks kandydata poza zakresem")
        if entry in seen:
            raise InvalidExtractionDraft("indeks kandydata powtórzony")
        seen.add(entry)
        ordered.append(entry)
    return ordered


def split_candidates_by_indexes(
    candidates: Sequence[object],
    indexes: list[int] | None,
) -> tuple[list[object], list[object]]:
    if indexes is None:
        return list(candidates), []
    chosen = [candidates[index] for index in indexes]
    skip = set(indexes)
    leftover = [row for position, row in enumerate(candidates) if position not in skip]
    return chosen, leftover


def require_extract_path(raw: object) -> str:
    if raw is None:
        return _PATH_TEXT
    if type(raw) is not str:
        raise InvalidExtractionDraft("extract_path musi być tekstem")
    token = raw.strip()
    if token not in _PATHS:
        raise InvalidExtractionDraft("extract_path spoza allowlisty")
    return token


def _golden_triple(row: object) -> tuple[str, str, str]:
    if type(row) is not dict:
        raise InvalidExtractionDraft("kandydat golden musi być obiektem")
    code = row.get("code")
    amount_text = row.get("amount_text")
    currency = row.get("currency")
    if type(code) is not str or type(amount_text) is not str or type(currency) is not str:
        raise InvalidExtractionDraft("kandydat golden: code, amount_text, currency")
    return (code, amount_text, currency)


def unmatched_golden_candidates(actual: object, expected: object) -> list[tuple[str, str, str]]:
    if type(actual) is not list or type(expected) is not list:
        raise InvalidExtractionDraft("listy kandydatów golden")
    got = {_golden_triple(row) for row in actual}
    missing: list[tuple[str, str, str]] = []
    for row in expected:
        triple = _golden_triple(row)
        if triple not in got:
            missing.append(triple)
    return missing


def require_rate_candidates_editable(draft_kind: object) -> None:
    if draft_kind not in {_RATE, _QUOTE, _RFP}:
        raise ExtractionCandidatesNotEditable(
            "edycja kandydatów tylko dla rate_line, carrier_quote albo tender_rfp",
        )


def bulk_accept_confidence_ok(raw: object, *, threshold: Decimal | None = None) -> bool:
    """Czy pewność kandydata pozwala na accept zbiorczy (domyślnie 0,70)."""
    minimum = threshold if threshold is not None else _BULK_MIN
    if type(raw) is not str:
        return False
    token = raw.strip().lower().replace(",", ".")
    if token == "":
        return False
    if token in _OK_BANDS:
        return True
    if token in _BAD_BANDS:
        return False
    if token.endswith("%"):
        try:
            value = Decimal(token[:-1].strip()) / Decimal(100)
        except InvalidOperation:
            return False
        return value >= minimum
    try:
        value = Decimal(token)
    except InvalidOperation:
        return False
    if value > Decimal(1):
        if value > Decimal(100):
            return False
        value = value / Decimal(100)
    return value >= minimum


def require_bulk_accept_confidence(
    candidates: Sequence[object],
    *,
    threshold: Decimal | None = None,
) -> None:
    """≥2 kandydatów: każdy musi przejść próg; jeden wiersz = HITL bez bramki."""
    minimum = threshold if threshold is not None else _BULK_MIN
    if len(candidates) < 2:
        return
    for index, row in enumerate(candidates):
        text = _confidence_text_of(row)
        if bulk_accept_confidence_ok(text, threshold=minimum):
            continue
        raise BulkAcceptConfidenceBelow(
            f"kandydat {index + 1}: pewność poniżej progu zbiorczego {minimum}",
        )


def _confidence_text_of(row: object) -> object:
    if isinstance(row, dict):
        return row.get("confidence_text", "")
    return getattr(row, "confidence_text", "")


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
