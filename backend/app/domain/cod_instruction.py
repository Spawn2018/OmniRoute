import re
from uuid import UUID

from app.domain.errors import InvalidCodInstruction

_CODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_STATUSES = frozenset({"noted", "advised", "collected", "refused"})
_MAX_REF = 256
_FIXTURE = "fixture://cod-instruction/"
_MANUAL = "tenant:manual"


def require_instruction_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCodInstruction("instruction_code musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE_PATTERN.fullmatch(token) is None:
        raise InvalidCodInstruction("kod instrukcji: snake 2–32")
    return token


def require_instruction_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidCodInstruction("shipment_id musi być UUID")
    return raw


def require_collection_status(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCodInstruction("collection_status musi być tekstem")
    token = raw.strip()
    if token not in _STATUSES:
        raise InvalidCodInstruction("nieznany status pobrania")
    return token


def require_instruction_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCodInstruction("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidCodInstruction("wskazanie zapisu pobrania")
    if len(token) > _MAX_REF:
        raise InvalidCodInstruction("wskazanie zapisu pobrania za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidCodInstruction("obce wskazanie zapisu pobrania")
    return token
