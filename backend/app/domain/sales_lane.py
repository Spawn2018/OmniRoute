import re

from app.domain.errors import InvalidSalesLane, InvalidUnlocode
from app.domain.port import normalize_unlocode

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"repeat", "spot", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://sales-lane/"
_REF_CAP = 256


def _parse_lane_pair(origin_raw: object, dest_raw: object) -> tuple[str, str]:
    if type(origin_raw) is not str or type(dest_raw) is not str:
        raise InvalidSalesLane("para miejsc musi być tekstem UN/LOCODE")
    try:
        origin = normalize_unlocode(origin_raw)
        dest = normalize_unlocode(dest_raw)
    except InvalidUnlocode as exc:
        raise InvalidSalesLane(f"para miejsc: {exc}") from exc
    if origin == dest:
        raise InvalidSalesLane("para miejsc nie może mieć tych samych końców")
    return origin, dest


def parse_sales_lane_row(
    code: object,
    kind: object,
    origin_ref: object,
    origin_raw: object,
    dest_raw: object,
) -> tuple[str, str, str, str, str]:
    if type(code) is not str:
        raise InvalidSalesLane("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidSalesLane("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidSalesLane("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidSalesLane("rodzaj: repeat, spot albo other")
    if type(origin_ref) is not str:
        raise InvalidSalesLane("obce source_ref")
    pointer = origin_ref.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidSalesLane("obce wskazanie zapisu korytarza")
    if len(pointer) > _REF_CAP:
        raise InvalidSalesLane("obce wskazanie zapisu korytarza za dlugie")
    origin, dest = _parse_lane_pair(origin_raw, dest_raw)
    return slug, token, pointer, origin, dest
