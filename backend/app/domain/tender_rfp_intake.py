import re
from uuid import UUID

from app.domain.errors import InvalidTenderRfpIntake

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_REF = 256
_FIXTURE = "fixture://tender-rfp-intake/"
_MANUAL = "tenant:manual"


def require_board_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderRfpIntake("tender_id musi być UUID")
    return raw


def require_intake_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderRfpIntake("przyjęcie musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidTenderRfpIntake("przyjęcie: snake 2–32")
    return token


def require_intake_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderRfpIntake("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTenderRfpIntake("wskazanie zapisu przyjęcia RFP")
    if len(token) > _MAX_REF:
        raise InvalidTenderRfpIntake("wskazanie zapisu przyjęcia RFP za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTenderRfpIntake("obce wskazanie zapisu przyjęcia RFP")
    return token
