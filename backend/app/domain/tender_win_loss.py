import re
from uuid import UUID

from app.domain.errors import InvalidTenderWinLoss

_OUTCOMES = frozenset({"won", "lost", "no_bid"})
_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_REF = 256
_FIXTURE = "fixture://tender-win-loss/"
_MANUAL = "tenant:manual"


def require_board_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderWinLoss("tender_id musi być UUID")
    return raw


def require_outcome(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderWinLoss("wynik musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if token not in _OUTCOMES:
        raise InvalidTenderWinLoss("wynik: won, lost albo no_bid")
    return token


def require_reason_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderWinLoss("powód musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidTenderWinLoss("powód: snake 2–32")
    return token


def require_verdict_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderWinLoss("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTenderWinLoss("wskazanie zapisu wyniku przetargu")
    if len(token) > _MAX_REF:
        raise InvalidTenderWinLoss("wskazanie zapisu wyniku przetargu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTenderWinLoss("obce wskazanie zapisu wyniku przetargu")
    return token
