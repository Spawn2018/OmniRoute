import re

from app.domain.errors import InvalidCarbonMethod

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_VERSION = re.compile(r"^[a-z0-9][a-z0-9_]{0,31}$")
_MAX_REF = 256
_FIXTURE = "fixture://carbon-method/"
_MANUAL = "tenant:manual"


def require_method_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCarbonMethod("metoda musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidCarbonMethod("metoda: snake 2–32")
    return token


def require_method_version(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCarbonMethod("wersja musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _VERSION.fullmatch(token) is None:
        raise InvalidCarbonMethod("wersja: token 1–32")
    return token


def require_carbon_method_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCarbonMethod("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidCarbonMethod("wskazanie zapisu metodyki CO2")
    if len(token) > _MAX_REF:
        raise InvalidCarbonMethod("wskazanie zapisu metodyki CO2 za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidCarbonMethod("obce wskazanie zapisu metodyki CO2")
    return token
