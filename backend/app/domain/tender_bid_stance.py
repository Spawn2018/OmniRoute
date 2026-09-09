from uuid import UUID

from app.domain.errors import InvalidTenderBidStance

_STANCES = frozenset({"bid", "no_bid"})
_MAX_REF = 256
_FIXTURE = "fixture://tender-bid-stance/"
_MANUAL = "tenant:manual"


def require_board_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderBidStance("tender_id musi być UUID")
    return raw


def require_stance_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderBidStance("udział musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if token not in _STANCES:
        raise InvalidTenderBidStance("udział: bid albo no_bid")
    return token


def require_stance_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderBidStance("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTenderBidStance("wskazanie zapisu postawy udziału")
    if len(token) > _MAX_REF:
        raise InvalidTenderBidStance("wskazanie zapisu postawy udziału za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTenderBidStance("obce wskazanie zapisu postawy udziału")
    return token
