import re

from app.domain.errors import InvalidTenantContractKek

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_WRAPS = frozenset({"password", "kms"})
_MAX_REF = 256
_FIXTURE = "fixture://kek/"
_MANUAL = "tenant:manual"


def require_kek_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenantContractKek("oznaczenie musi być tekstem")
    token = raw.strip()
    if _CODE.fullmatch(token) is None:
        raise InvalidTenantContractKek("oznaczenie: snake 2–32")
    return token


def require_wrap_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenantContractKek("owijka musi być tekstem")
    token = raw.strip().lower()
    if token not in _WRAPS:
        raise InvalidTenantContractKek("owijka: allowlista HITL")
    return token


def require_kek_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTenantContractKek("obce source_ref")
    token = raw.strip()
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTenantContractKek("obce wskazanie zapisu znacznika KEK")
    if len(token) > _MAX_REF:
        raise InvalidTenantContractKek("obce wskazanie zapisu znacznika KEK za długie")
    return token
