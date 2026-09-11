import re

from app.domain.errors import InvalidLoadPlanMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"axes", "tunnel", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://load-plan-mark/"
_REF_CAP = 256


def parse_load_plan_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidLoadPlanMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidLoadPlanMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidLoadPlanMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidLoadPlanMark(
            "rodzaj: axes, tunnel albo other",
        )
    if type(origin) is not str:
        raise InvalidLoadPlanMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidLoadPlanMark("obce wskazanie zapisu znacznika planu załadunku")
    if len(pointer) > _REF_CAP:
        raise InvalidLoadPlanMark("obce wskazanie zapisu znacznika planu załadunku za długie")
    return slug, token, pointer
