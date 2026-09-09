from uuid import UUID

from app.domain.errors import InvalidTenderCarbonMark

_MARKS = frozenset({"declared", "exempt"})
_MAX_REF = 256
_FIXTURE = "fixture://tender-carbon-mark/"
_MANUAL = "tenant:manual"


def require_board_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderCarbonMark("tender_id musi być UUID")
    return raw


def require_mark_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderCarbonMark("ślad musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if token not in _MARKS:
        raise InvalidTenderCarbonMark("ślad: declared albo exempt")
    return token


def require_carbon_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderCarbonMark("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTenderCarbonMark("wskazanie zapisu znacznika śladu")
    if len(token) > _MAX_REF:
        raise InvalidTenderCarbonMark("wskazanie zapisu znacznika śladu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTenderCarbonMark("obce wskazanie zapisu znacznika śladu")
    return token
