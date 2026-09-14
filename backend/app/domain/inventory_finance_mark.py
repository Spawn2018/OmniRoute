import re

from app.domain.errors import InvalidInventoryFinanceMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"valuation", "aging", "release", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://inventory-finance/"
_REF_CAP = 256


def parse_inventory_finance_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidInventoryFinanceMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidInventoryFinanceMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidInventoryFinanceMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidInventoryFinanceMark(
            "rodzaj: valuation, aging, release albo other",
        )
    if type(origin) is not str:
        raise InvalidInventoryFinanceMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidInventoryFinanceMark(
            "obce wskazanie zapisu zapasu finansowego",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidInventoryFinanceMark(
            "obce wskazanie zapisu zapasu finansowego za dlugie",
        )
    return slug, token, pointer
