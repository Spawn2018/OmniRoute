import re

from app.domain.errors import InvalidSalesLane

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"repeat", "spot", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://sales-lane/"
_REF_CAP = 256


def parse_sales_lane_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
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
    if type(origin) is not str:
        raise InvalidSalesLane("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidSalesLane("obce wskazanie zapisu korytarza")
    if len(pointer) > _REF_CAP:
        raise InvalidSalesLane("obce wskazanie zapisu korytarza za dlugie")
    return slug, token, pointer
