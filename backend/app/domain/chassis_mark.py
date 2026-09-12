import re

from app.domain.errors import InvalidChassisMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_CHASSIS_KINDS = frozenset({"chassis", "trailer", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://chassis-mark/"


def parse_chassis_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidChassisMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidChassisMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidChassisMark("rodzaj chassis musi być tekstem")
    token = kind.strip().lower()
    if token not in _CHASSIS_KINDS:
        raise InvalidChassisMark(
            "rodzaj chassis: chassis, trailer albo other",
        )
    if type(origin) is not str:
        raise InvalidChassisMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidChassisMark(
            "obce wskazanie zapisu znacznika chassis",
        )
    if len(pointer) > 256:
        raise InvalidChassisMark(
            "obce wskazanie zapisu znacznika chassis za długie",
        )
    return slug, token, pointer
