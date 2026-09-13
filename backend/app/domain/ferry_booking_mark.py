import re

from app.domain.errors import InvalidFerryBookingMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"booking", "window", "sailing", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://ferry-booking-mark/"
_REF_CAP = 256


def parse_ferry_booking_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidFerryBookingMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidFerryBookingMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidFerryBookingMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidFerryBookingMark("rodzaj: booking, window, sailing albo other")
    if type(origin) is not str:
        raise InvalidFerryBookingMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidFerryBookingMark("obce wskazanie zapisu rezerwacji promu")
    if len(pointer) > _REF_CAP:
        raise InvalidFerryBookingMark("obce wskazanie zapisu rezerwacji promu za dlugie")
    return slug, token, pointer
