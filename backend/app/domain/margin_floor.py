import re
from dataclasses import dataclass
from decimal import Decimal

from app.domain.errors import InvalidMarginFloor, InvalidMoney, InvalidUnlocode
from app.domain.money import Money
from app.domain.port import normalize_unlocode

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_FIX = "fixture://margin-floor/"


@dataclass(frozen=True)
class MarginFloorDraft:
    floor_code: str
    origin_unlocode: str
    destination_unlocode: str
    floor_amount: Decimal
    floor_currency: str
    source_ref: str


def _snake(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidMarginFloor("oznaczenie musi być tekstem")
    token = raw.strip()
    if _CODE.fullmatch(token) is None:
        raise InvalidMarginFloor("oznaczenie: snake 2–32")
    return token


def _lane_pair(origin_raw: object, dest_raw: object) -> tuple[str, str]:
    if type(origin_raw) is not str or type(dest_raw) is not str:
        raise InvalidMarginFloor("para miejsc musi być tekstem UN/LOCODE")
    try:
        origin = normalize_unlocode(origin_raw)
        dest = normalize_unlocode(dest_raw)
    except InvalidUnlocode as exc:
        raise InvalidMarginFloor(f"para miejsc: {exc}") from exc
    if origin == dest:
        raise InvalidMarginFloor("para miejsc nie może mieć tych samych końców")
    return origin, dest


def _floor_money(amount: object, currency: object) -> Money:
    try:
        return Money.of(amount, currency)
    except InvalidMoney as exc:
        raise InvalidMarginFloor(str(exc)) from exc


def _source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidMarginFloor("obce source_ref")
    pointer = raw.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidMarginFloor("obce wskazanie zapisu podłogi marży")
    if len(pointer) > 256:
        raise InvalidMarginFloor("obce wskazanie zapisu podłogi marży za długie")
    return pointer


def parse_margin_floor_row(
    floor_code: object,
    origin_unlocode: object,
    destination_unlocode: object,
    floor_amount: object,
    floor_currency: object,
    source_ref: object,
) -> MarginFloorDraft:
    money = _floor_money(floor_amount, floor_currency)
    origin, dest = _lane_pair(origin_unlocode, destination_unlocode)
    return MarginFloorDraft(
        floor_code=_snake(floor_code),
        origin_unlocode=origin,
        destination_unlocode=dest,
        floor_amount=money.amount,
        floor_currency=money.currency.code,
        source_ref=_source_ref(source_ref),
    )
