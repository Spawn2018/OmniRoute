import re

from app.domain.errors import InvalidRfidMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"reader", "gate", "tag", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://rfid/"
_REF_CAP = 256


def parse_rfid_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidRfidMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidRfidMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidRfidMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidRfidMark(
            "rodzaj: reader, gate, tag albo other",
        )
    if type(origin) is not str:
        raise InvalidRfidMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidRfidMark("obce wskazanie zapisu RFID")
    if len(pointer) > _REF_CAP:
        raise InvalidRfidMark("obce wskazanie zapisu RFID za dlugie")
    return slug, token, pointer
