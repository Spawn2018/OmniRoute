import re
from uuid import UUID

from app.domain.errors import InvalidTenderPlaybook

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_TEXT = 512
_MAX_REF = 256
_FIXTURE = "fixture://tender-playbook/"
_MANUAL = "tenant:manual"


def require_board_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidTenderPlaybook("tender_id musi być UUID")
    return raw


def require_claim_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderPlaybook("teza musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidTenderPlaybook("teza: snake 2–32")
    return token


def require_claim_text(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderPlaybook("twierdzenie musi być tekstem")
    token = raw.strip()
    if token == "" or len(token) > _MAX_TEXT:
        raise InvalidTenderPlaybook("twierdzenie: 1–512 znaków")
    return token


def require_play_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenderPlaybook("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTenderPlaybook("wskazanie zapisu playbooka")
    if len(token) > _MAX_REF:
        raise InvalidTenderPlaybook("wskazanie zapisu playbooka za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTenderPlaybook("obce wskazanie zapisu playbooka")
    return token
