import re
from decimal import Decimal, InvalidOperation

from app.domain.container import require_iso_size_type
from app.domain.errors import InvalidContainer, InvalidLocalCharge, InvalidUnlocode
from app.domain.port import normalize_unlocode

_KINDS = frozenset({"thc", "isps", "seal", "amendment"})
_CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")
_MAX_REF = 256
_FIXTURE = "fixture://local-charge/"
_MANUAL = "tenant:manual"
_FOUR = Decimal("0.0001")


def require_levy_kind(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidLocalCharge("rodzaj dopłaty musi być tekstem")
    token = raw.strip().lower()
    if token not in _KINDS:
        raise InvalidLocalCharge("nieznany rodzaj dopłaty")
    return token


def require_levy_amount(raw: object) -> Decimal:
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidLocalCharge("kwota nie może być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidLocalCharge("kwota musi być liczbą dziesiętną")
    try:
        parsed = raw if isinstance(raw, Decimal) else Decimal(str(raw))
    except InvalidOperation as exc:
        raise InvalidLocalCharge("kwota musi być liczbą dziesiętną") from exc
    if parsed <= 0:
        raise InvalidLocalCharge("kwota musi być dodatnia")
    return parsed.quantize(_FOUR)


def require_levy_currency(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidLocalCharge("waluta dopłaty musi być tekstem")
    token = raw.strip().upper()
    if _CURRENCY_PATTERN.fullmatch(token) is None:
        raise InvalidLocalCharge("waluta dopłaty: ISO 4217, trzy litery")
    return token


def require_levy_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidLocalCharge("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidLocalCharge("wskazanie zapisu dopłaty lokalnej")
    if len(token) > _MAX_REF:
        raise InvalidLocalCharge("wskazanie zapisu dopłaty lokalnej za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidLocalCharge("obce wskazanie zapisu dopłaty lokalnej")
    return token


def require_levy_port(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidLocalCharge("port musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    try:
        return normalize_unlocode(token)
    except InvalidUnlocode as exc:
        raise InvalidLocalCharge("port: UN/LOCODE 5 znaków") from exc


def require_levy_iso(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidLocalCharge("typ musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    try:
        return require_iso_size_type(token)
    except InvalidContainer as exc:
        raise InvalidLocalCharge("typ: ISO size/type 4 znaki") from exc


_MAX_LABEL = 64


def require_levy_carrier_label(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidLocalCharge("armator musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_LABEL:
        raise InvalidLocalCharge("armator za długi")
    return token


def require_levy_service_label(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidLocalCharge("serwis musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_LABEL:
        raise InvalidLocalCharge("serwis za długi")
    return token
