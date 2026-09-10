import re
from decimal import Decimal, InvalidOperation
from uuid import UUID

from app.domain.errors import InvalidTrip

_STATUSES = frozenset({"draft", "planned", "in_transit", "completed", "cancelled"})
_FREEZE = frozenset({"in_transit", "completed"})
_SLOTS = frozenset({"vehicle", "trailer", "driver"})
_MAX_NO = 64
_MAX_REF = 256
_MAX_ROUTE = 128
_FIXTURE = "fixture://trip/"
_MANUAL = "tenant:manual"
_CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")
_FOUR = Decimal("0.0001")


def require_trip_no(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTrip("trip_no musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTrip("numer przejazdu")
    if len(token) > _MAX_NO:
        raise InvalidTrip("numer przejazdu za długi")
    return token


def require_trip_status(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTrip("status musi być tekstem")
    token = raw.strip()
    if token not in _STATUSES:
        raise InvalidTrip("nieznany status przejazdu")
    return token


def require_trip_resource_id(raw: object) -> UUID | None:
    if raw is None:
        return None
    if type(raw) is not UUID:
        raise InvalidTrip("wskazanie zasobu musi być UUID")
    return raw


def require_trip_slot(slot: object, resource_kind: object) -> None:
    if type(slot) is not str or slot not in _SLOTS:
        raise InvalidTrip("nieznany slot floty")
    if type(resource_kind) is not str or resource_kind != slot:
        raise InvalidTrip("rodzaj zasobu nie pasuje")


def require_distinct_drivers(driver_id: UUID | None, driver2_id: UUID | None) -> None:
    if driver2_id is None:
        return
    if driver_id == driver2_id:
        raise InvalidTrip("ten sam kierowca na obu fotelach")


def require_trip_source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTrip("source_ref musi być tekstem")
    token = raw.strip()
    if token == "":
        raise InvalidTrip("wskazanie zapisu przejazdu")
    if len(token) > _MAX_REF:
        raise InvalidTrip("wskazanie zapisu przejazdu za długie")
    if token != _MANUAL and not token.startswith(_FIXTURE):
        raise InvalidTrip("obce wskazanie zapisu przejazdu")
    return token


def require_route_label(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidTrip("trasa przejazdu musi być tekstem")
    token = raw.strip()
    if token == "":
        return None
    if len(token) > _MAX_ROUTE:
        raise InvalidTrip("trasa przejazdu za długa")
    return token


def require_trip_planned_distance_km(raw: object) -> Decimal | None:
    if raw is None:
        return None
    if type(raw) is str and raw.strip() == "":
        return None
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidTrip("km nie może być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidTrip("km musi być liczbą dziesiętną")
    try:
        parsed = raw if isinstance(raw, Decimal) else Decimal(str(raw))
    except InvalidOperation as exc:
        raise InvalidTrip("km musi być liczbą dziesiętną") from exc
    if parsed < 0:
        raise InvalidTrip("km nie może być ujemne")
    return parsed.quantize(_FOUR)


def require_trip_actual_distance_km(raw: object) -> Decimal | None:
    return require_trip_planned_distance_km(raw)


def _require_buy_amount(raw: object) -> Decimal:
    if isinstance(raw, float) or isinstance(raw, bool):
        raise InvalidTrip("kwota nie może być float")
    if not isinstance(raw, Decimal | str | int):
        raise InvalidTrip("kwota snapshotu musi być liczbą dziesiętną")
    try:
        parsed = raw if isinstance(raw, Decimal) else Decimal(str(raw))
    except InvalidOperation as exc:
        raise InvalidTrip("kwota snapshotu musi być liczbą dziesiętną") from exc
    if parsed <= 0:
        raise InvalidTrip("kwota snapshotu musi być dodatnia")
    return parsed.quantize(_FOUR)


def _require_buy_currency(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTrip("waluta snapshotu musi być tekstem")
    token = raw.strip().upper()
    if _CURRENCY_PATTERN.fullmatch(token) is None:
        raise InvalidTrip("waluta snapshotu: ISO 4217, trzy litery")
    return token


def require_expected_buy(
    status: str,
    amount: object,
    currency: object,
) -> tuple[Decimal | None, str | None]:
    if status in _FREEZE:
        if amount is None or (type(amount) is str and amount.strip() == ""):
            raise InvalidTrip("kwota snapshotu wymagana w drodze")
        return _require_buy_amount(amount), _require_buy_currency(currency)
    if amount is not None or currency is not None:
        raise InvalidTrip("snapshot kosztu tylko przy w drodze")
    return None, None
