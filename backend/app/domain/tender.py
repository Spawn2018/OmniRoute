from datetime import date
from uuid import UUID

from app.domain.errors import InvalidTender

_MAX_REF = 256
_FIXTURE = "fixture://tender/"
_MANUAL = "tenant:manual"
_SIDES = frozenset({"sell", "buy"})
_KINDS = frozenset({"open", "restricted", "sealed", "e_auction"})
_STATUSES = frozenset({"draft", "open", "awarded", "lost", "no_bid"})
_INCOTERMS = frozenset(
    {"EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF"},
)
_TRADE_SIDES = frozenset({"import", "export"})
_PLACE_RULES = frozenset({"DAP", "DDP"})


def require_buyer_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTender("nabywca musi być UUID")
    return raw


def require_side(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTender("strona przetargu musi być tekstem")
    token = raw.strip()
    if token not in _SIDES:
        raise InvalidTender("nieznana strona przetargu")
    return token


def require_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTender("rodzaj przetargu musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidTender("nieznany rodzaj przetargu")
    return token


def require_status(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTender("status przetargu musi być tekstem")
    token = raw.strip()
    if token not in _STATUSES:
        raise InvalidTender("nieznany status przetargu")
    return token


def require_deadline_at(raw: object) -> date:
    if type(raw) is not str:
        raise InvalidTender("termin musi być dniem")
    token = raw.strip()
    if token == "":
        raise InvalidTender("termin musi być dniem")
    try:
        return date.fromisoformat(token)
    except ValueError as exc:
        raise InvalidTender("termin musi być dniem ISO") from exc


def require_incoterm(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTender("incoterm musi być tekstem")
    token = raw.strip().upper()
    if token not in _INCOTERMS:
        raise InvalidTender("nieznany incoterm")
    return token


def require_trade_side(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTender("strona handlu musi być tekstem")
    token = raw.strip()
    if token not in _TRADE_SIDES:
        raise InvalidTender("nieznana strona handlu")
    return token


def require_named_place(incoterm: str, raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTender("miejsce musi być tekstem")
    token = raw.strip()
    if incoterm in _PLACE_RULES and token == "":
        raise InvalidTender("miejsce wymagane przy DAP/DDP")
    return token


def require_board_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTender("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTender("wskazanie zapisu przetargu")
    if len(token) > _MAX_REF:
        raise InvalidTender("wskazanie zapisu przetargu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTender("obce wskazanie zapisu przetargu")
    return token
