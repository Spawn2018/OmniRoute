import re
from uuid import UUID

from app.domain.errors import InvalidOceanBill

_BILL_NO = re.compile(r"^[A-Za-z0-9-]{2,32}$")
_KINDS = frozenset({"hbl", "mbl"})
_MAX_REF = 256
_FIXTURE = "fixture://ocean-bill/"
_MANUAL = "tenant:manual"


def require_bill_no(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOceanBill("bill_no musi być tekstem")
    token = raw.strip()
    if _BILL_NO.fullmatch(token) is None:
        raise InvalidOceanBill("numer konosamentu: 2–32 litery cyfry myślnik")
    return token


def require_bill_shipment_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidOceanBill("shipment_id musi być UUID")
    return raw


def require_bill_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOceanBill("bill_kind musi być tekstem")
    token = raw.strip()
    if token not in _KINDS:
        raise InvalidOceanBill("nieznany rodzaj konosamentu")
    return token


def require_bill_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidOceanBill("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidOceanBill("wskazanie zapisu konosamentu")
    if len(token) > _MAX_REF:
        raise InvalidOceanBill("wskazanie zapisu konosamentu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidOceanBill("obce wskazanie zapisu konosamentu")
    return token
