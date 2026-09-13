import re

from app.domain.errors import InvalidRoutePlanMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"route", "stop", "window", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://route-plan-mark/"
_REF_CAP = 256


def parse_route_plan_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidRoutePlanMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidRoutePlanMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidRoutePlanMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidRoutePlanMark("rodzaj: route, stop, window albo other")
    if type(origin) is not str:
        raise InvalidRoutePlanMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidRoutePlanMark("obce wskazanie zapisu znacznika planu trasy")
    if len(pointer) > _REF_CAP:
        raise InvalidRoutePlanMark("obce wskazanie zapisu znacznika planu trasy za długie")
    return slug, token, pointer
