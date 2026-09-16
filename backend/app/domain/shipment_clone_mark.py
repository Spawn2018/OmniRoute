import re

from app.domain.errors import InvalidShipmentCloneMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"last_similar", "manual_pick", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://shipment-clone-mark/"
_REF_CAP = 256


def parse_shipment_clone_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidShipmentCloneMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidShipmentCloneMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidShipmentCloneMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidShipmentCloneMark(
            "rodzaj: last_similar, manual_pick albo other",
        )
    if type(origin) is not str:
        raise InvalidShipmentCloneMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidShipmentCloneMark(
            "obce wskazanie zapisu intencji klonu",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidShipmentCloneMark(
            "obce wskazanie zapisu intencji klonu za długie",
        )
    return slug, token, pointer
