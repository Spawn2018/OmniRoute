import re

from app.domain.errors import InvalidEDeliveryMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"edor", "registered", "receipt", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://e-delivery-mark/"
_REF_CAP = 256


def parse_e_delivery_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidEDeliveryMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidEDeliveryMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidEDeliveryMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidEDeliveryMark(
            "rodzaj: edor, registered, receipt albo other",
        )
    if type(origin) is not str:
        raise InvalidEDeliveryMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidEDeliveryMark("obce wskazanie zapisu znacznika e-delivery")
    if len(pointer) > _REF_CAP:
        raise InvalidEDeliveryMark(
            "obce wskazanie zapisu znacznika e-delivery za długie",
        )
    return slug, token, pointer
