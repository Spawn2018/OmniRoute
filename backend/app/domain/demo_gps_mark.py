import re

from app.domain.errors import InvalidDemoGpsMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_DEMO_KINDS = frozenset({"seven_day", "fleet_demo", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://demo-gps-mark/"


def parse_demo_gps_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidDemoGpsMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidDemoGpsMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidDemoGpsMark("rodzaj demo musi być tekstem")
    token = kind.strip().lower()
    if token not in _DEMO_KINDS:
        raise InvalidDemoGpsMark("rodzaj demo: seven_day, fleet_demo albo other")
    if type(origin) is not str:
        raise InvalidDemoGpsMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidDemoGpsMark("obce wskazanie zapisu znacznika demo GPS")
    if len(pointer) > 256:
        raise InvalidDemoGpsMark("obce wskazanie zapisu znacznika demo GPS za długie")
    return slug, token, pointer
