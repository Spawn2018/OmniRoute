from uuid import UUID

from app.domain.errors import InvalidTenderConsortiumMember

_SEATS = frozenset({"lead", "member"})
_MAX_REF = 256
_FIXTURE = "fixture://tender-consortium-member/"
_MANUAL = "tenant:manual"


def require_board_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderConsortiumMember("tender_id musi być UUID")
    return raw


def require_party_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderConsortiumMember("party_id musi być UUID")
    return raw


def require_seat_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderConsortiumMember("fotel musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if token not in _SEATS:
        raise InvalidTenderConsortiumMember("fotel: lead albo member")
    return token


def require_seat_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderConsortiumMember("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTenderConsortiumMember("wskazanie zapisu fotela konsorcjum")
    if len(token) > _MAX_REF:
        raise InvalidTenderConsortiumMember("wskazanie zapisu fotela konsorcjum za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTenderConsortiumMember("obce wskazanie zapisu fotela konsorcjum")
    return token
