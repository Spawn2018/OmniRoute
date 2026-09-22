import re
from decimal import Decimal, InvalidOperation
from uuid import UUID

from app.domain.errors import InvalidGroupageTariff
from app.domain.location import LocationKind

_CODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")
_MAX_REF = 256
_FIXTURE = "fixture://groupage-tariff/"
_MANUAL = "tenant:manual"
_FOUR = Decimal("0.0001")


def require_tariff_code(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidGroupageTariff("tariff_code musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE_PATTERN.fullmatch(token) is None:
        raise InvalidGroupageTariff("kod cennika: snake 2–32")
    return token


def require_tariff_location_id(raw: object) -> UUID:
    if type(raw) is not UUID:
        raise InvalidGroupageTariff("location_id musi być UUID")
    return raw


def require_postal_zone_kind(kind: object) -> str:
    if type(kind) is not str:
        raise InvalidGroupageTariff("rodzaj lokalizacji musi być tekstem")
    if kind != LocationKind.POSTAL_ZONE.value:
        raise InvalidGroupageTariff("cennik drobnicy: tylko strefa taryfowa postal_zone")
    return kind


def _decimal(raw: object, *, field: str) -> Decimal:
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidGroupageTariff(f"{field} nie może być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidGroupageTariff(f"{field} musi być liczbą dziesiętną")
    try:
        parsed = raw if isinstance(raw, Decimal) else Decimal(str(raw))
    except InvalidOperation as exc:
        raise InvalidGroupageTariff(f"{field} musi być liczbą dziesiętną") from exc
    if parsed <= 0:
        raise InvalidGroupageTariff(f"{field} musi być dodatnia")
    return parsed.quantize(_FOUR)


def require_chargeable_weight(raw: object) -> Decimal:
    return _decimal(raw, field="chargeable_weight")


def require_tariff_amount(raw: object) -> Decimal:
    return _decimal(raw, field="amount")


def require_tariff_volume_m3(raw: object) -> Decimal | None:
    if raw is None:
        return None
    if type(raw) is str and raw.strip() == "":
        return None
    return _decimal(raw, field="objętość")


def require_tariff_currency(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidGroupageTariff("waluta cennika musi być tekstem")
    token = raw.strip().upper()
    if _CURRENCY_PATTERN.fullmatch(token) is None:
        raise InvalidGroupageTariff("waluta cennika: ISO 4217, trzy litery")
    return token


def require_tariff_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidGroupageTariff("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidGroupageTariff("wskazanie zapisu cennika")
    if len(token) > _MAX_REF:
        raise InvalidGroupageTariff("wskazanie zapisu cennika za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidGroupageTariff("obce wskazanie zapisu cennika")
    return token
