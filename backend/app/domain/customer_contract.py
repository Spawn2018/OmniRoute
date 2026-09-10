import re

from app.domain.errors import InvalidCustomerContract

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MAX_LABEL = 128
_MAX_REF = 256
_FIXTURE = "fixture://contract/"
_MANUAL = "tenant:manual"


def require_contract_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCustomerContract("oznaczenie musi być tekstem")
    token = raw.strip()
    if _CODE.fullmatch(token) is None:
        raise InvalidCustomerContract("oznaczenie: snake 2–32")
    return token


def require_shipper_label(raw: object) -> str:
    return _require_label(raw, "załadowca")


def require_their_customer_label(raw: object) -> str:
    return _require_label(raw, "odbiorca")


def _require_label(raw: object, token: str) -> str:
    if type(raw) is not str:
        raise InvalidCustomerContract(f"{token} musi być tekstem")
    label = raw.strip()
    if not label or len(label) > _MAX_LABEL:
        raise InvalidCustomerContract(f"{token}: tekst 1–128")
    return label


def require_contract_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidCustomerContract("obce source_ref")
    token = raw.strip()
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidCustomerContract("obce wskazanie zapisu umowy klienta")
    if len(token) > _MAX_REF:
        raise InvalidCustomerContract("obce wskazanie zapisu umowy klienta za długie")
    return token
