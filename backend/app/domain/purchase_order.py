import re

from app.domain.errors import InvalidPurchaseOrder

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_PREFIX = "fixture://purchase-order/"
_REF_CAP = 256
_MAX_PLANT = 128


def parse_purchase_order_row(
    code: object, plant: object, origin: object
) -> tuple[str, str | None, str]:
    if type(code) is not str:
        raise InvalidPurchaseOrder("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidPurchaseOrder("oznaczenie: snake 2–32")
    if type(origin) is not str:
        raise InvalidPurchaseOrder("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidPurchaseOrder("obce wskazanie zapisu zamówienia zakupu")
    if len(pointer) > _REF_CAP:
        raise InvalidPurchaseOrder("obce wskazanie zapisu zamówienia zakupu za długie")
    return slug, _optional_plant(plant), pointer


def _optional_plant(raw: object) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidPurchaseOrder("zakład musi być tekstem")
    label = raw.strip()
    if not label:
        return None
    if len(label) > _MAX_PLANT:
        raise InvalidPurchaseOrder("zakład: tekst 1–128")
    return label
