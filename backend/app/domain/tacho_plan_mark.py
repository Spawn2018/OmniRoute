import re

from app.domain.errors import InvalidTachoPlanMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"plan", "window", "rest", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://tacho-plan-mark/"
_REF_CAP = 256


def parse_tacho_plan_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidTachoPlanMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidTachoPlanMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidTachoPlanMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidTachoPlanMark("rodzaj: plan, window, rest albo other")
    if type(origin) is not str:
        raise InvalidTachoPlanMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidTachoPlanMark("obce wskazanie zapisu ograniczenia tacho")
    if len(pointer) > _REF_CAP:
        raise InvalidTachoPlanMark("obce wskazanie zapisu ograniczenia tacho za dlugie")
    return slug, token, pointer
