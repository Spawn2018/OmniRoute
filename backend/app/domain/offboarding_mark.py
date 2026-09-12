import re

from app.domain.errors import InvalidOffboardingMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"offboard", "export", "revoke", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://offboarding-mark/"
_REF_CAP = 256


def parse_offboarding_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidOffboardingMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidOffboardingMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidOffboardingMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidOffboardingMark(
            "rodzaj: offboard, export, revoke albo other",
        )
    if type(origin) is not str:
        raise InvalidOffboardingMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidOffboardingMark("obce wskazanie zapisu znacznika offboarding")
    if len(pointer) > _REF_CAP:
        raise InvalidOffboardingMark(
            "obce wskazanie zapisu znacznika offboarding za długie",
        )
    return slug, token, pointer
