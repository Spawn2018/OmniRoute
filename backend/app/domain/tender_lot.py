from uuid import UUID

from app.domain.errors import InvalidTenderLot

_MAX_REF = 256
_MAX_CODE = 32
_FIXTURE = "fixture://tender-lot/"
_MANUAL = "tenant:manual"


def require_tender_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderLot("tender_id musi być UUID")
    return raw


def require_lot_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderLot("partia musi być tekstem")
    token = raw.strip()
    if token == "" or len(token) > _MAX_CODE:
        raise InvalidTenderLot("partia musi być kodem")
    return token


def require_lot_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderLot("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTenderLot("wskazanie zapisu partii przetargu")
    if len(token) > _MAX_REF:
        raise InvalidTenderLot("wskazanie zapisu partii przetargu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTenderLot("obce wskazanie zapisu partii przetargu")
    return token
