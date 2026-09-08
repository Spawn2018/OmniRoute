from uuid import UUID

from app.domain.errors import InvalidTenderDataRoom

_MAX_REF = 256
_FIXTURE = "fixture://tender-data-room/"
_MANUAL = "tenant:manual"
_SIGNED = "signed"


def require_board_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderDataRoom("tender_id musi być UUID")
    return raw


def require_nda_mark(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderDataRoom("nda musi być tekstem signed")
    token = raw.strip()
    if token != _SIGNED:
        raise InvalidTenderDataRoom("nda musi być signed")
    return token


def require_room_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderDataRoom("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTenderDataRoom("wskazanie zapisu pokoju danych")
    if len(token) > _MAX_REF:
        raise InvalidTenderDataRoom("wskazanie zapisu pokoju danych za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTenderDataRoom("obce wskazanie zapisu pokoju danych")
    return token
