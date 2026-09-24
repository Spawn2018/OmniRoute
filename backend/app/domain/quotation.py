from datetime import date
from uuid import UUID

from app.domain.charge_code import normalize_aliases
from app.domain.errors import (
    IncompleteQuotationSnapshot,
    InvalidQuotation,
    InvalidQuotationBatch,
    InvalidQuotationDocumentNumber,
    InvalidQuotationIncoterm,
    MissingQuotationPrefix,
    QuotationNamedPlaceRequired,
)

_INCOTERMS = frozenset(
    {"EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"},
)
_INCOTERM_VERSIONS = frozenset({"2020", "2010"})
_TRADE_SIDES = frozenset({"import", "export"})
_PLACE_RULES = frozenset({"DAP", "DDP"})

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


def require_document_number_prefix(raw: str | None) -> str:
    if raw is None:
        raise MissingQuotationPrefix("nadanie numeru wymaga prefiksu w ustawieniach")
    token = raw.strip()
    if token == "":
        raise MissingQuotationPrefix("nadanie numeru wymaga prefiksu w ustawieniach")
    return token


def require_quotation_incoterm(
    incoterm: object = None,
    incoterms_version: object = None,
    trade_side: object = None,
    named_place: object = None,
) -> tuple[str | None, str | None, str | None, str | None]:
    blank = (incoterm, incoterms_version, trade_side, named_place)
    if blank == (None, None, None, None):
        return None, None, None, None
    rule = _optional_token(incoterm, field="incoterm", allowed=_INCOTERMS)
    version = _optional_token(
        incoterms_version,
        field="incoterms_version",
        allowed=_INCOTERM_VERSIONS,
    )
    side = _optional_token(trade_side, field="trade_side", allowed=_TRADE_SIDES)
    place = _optional_place(named_place)
    if rule is None or version is None or side is None:
        raise InvalidQuotationIncoterm("incoterm wymaga reguły, wersji i strony handlu")
    if rule in _PLACE_RULES and place is None:
        raise QuotationNamedPlaceRequired("DAP/DDP wymaga named_place")
    return rule, version, side, place


def _optional_token(raw: object, *, field: str, allowed: frozenset[str]) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidQuotationIncoterm(f"{field} musi być tekstem")
    token = raw.strip().upper() if field == "incoterm" else raw.strip()
    if field == "trade_side":
        token = raw.strip().casefold()
    if token not in allowed:
        raise InvalidQuotationIncoterm(f"{field} spoza allowlisty")
    return token


def _optional_place(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidQuotationIncoterm("named_place musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    return token


def require_valid_until(raw: object) -> date | None:
    if raw is None:
        return None
    if type(raw) is date:
        return raw
    if type(raw) is not str:
        raise InvalidQuotation("ważność: data kalendarzowa")
    token = raw.strip()
    if token == "":
        return None
    try:
        return date.fromisoformat(token)
    except ValueError as exc:
        raise InvalidQuotation("ważność: data kalendarzowa") from exc


def format_quotation_document_number(prefix: str, sequence: int) -> str:
    token = require_document_number_prefix(prefix)
    if sequence < 1:
        raise InvalidQuotationDocumentNumber("numer oferty liczy Postgres od 1")
    rendered = f"{token}{sequence:04d}"
    if len(rendered) > 32:
        raise InvalidQuotationDocumentNumber("numer oferty: max 32 znaki")
    return rendered

