from uuid import UUID

from app.domain.errors import InvalidTenderRound

_MAX_REF = 256
_FIXTURE = "fixture://tender-round/"
_MANUAL = "tenant:manual"


def require_board_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderRound("tender_id musi być UUID")
    return raw


def require_round_no(raw: object) -> int:
    if type(raw) is not int:
        raise InvalidTenderRound("runda musi być liczbą całkowitą")
    if raw < 1:
        raise InvalidTenderRound("runda musi być dodatnia")
    return raw


def require_round_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderRound("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTenderRound("wskazanie zapisu rundy przetargu")
    if len(token) > _MAX_REF:
        raise InvalidTenderRound("wskazanie zapisu rundy przetargu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTenderRound("obce wskazanie zapisu rundy przetargu")
    return token
