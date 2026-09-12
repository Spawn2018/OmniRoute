import re

from app.domain.errors import InvalidLabelParkingMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_PARKING_KINDS = frozenset({"secure", "labeled", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://label-parking-mark/"


def parse_label_parking_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidLabelParkingMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidLabelParkingMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidLabelParkingMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _PARKING_KINDS:
        raise InvalidLabelParkingMark("rodzaj: secure, labeled albo other")
    if type(origin) is not str:
        raise InvalidLabelParkingMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidLabelParkingMark("obce wskazanie zapisu znacznika LABEL parking")
    if len(pointer) > 256:
        raise InvalidLabelParkingMark("obce wskazanie zapisu znacznika LABEL parking za długie")
    return slug, token, pointer
