import re
from uuid import UUID

from app.domain.errors import InvalidTenderProspect

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_REF = 256
_FIXTURE = "fixture://tender-prospect/"
_MANUAL = "tenant:manual"


def require_board_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderProspect("tender_id musi być UUID")
    return raw


def require_party_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderProspect("party_id musi być UUID")
    return raw


def require_outreach_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderProspect("prospekt musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidTenderProspect("prospekt: snake 2–32")
    return token


def require_prospect_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderProspect("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTenderProspect("wskazanie zapisu prospektu")
    if len(token) > _MAX_REF:
        raise InvalidTenderProspect("wskazanie zapisu prospektu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTenderProspect("obce wskazanie zapisu prospektu")
    return token
