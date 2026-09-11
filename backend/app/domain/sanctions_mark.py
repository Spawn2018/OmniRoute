import re

from app.domain.errors import InvalidSanctionsMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"ofac", "eu", "un", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://sanctions-mark/"
_REF_CAP = 256


def parse_sanctions_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidSanctionsMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidSanctionsMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidSanctionsMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidSanctionsMark(
            "rodzaj: ofac, eu, un albo other",
        )
    if type(origin) is not str:
        raise InvalidSanctionsMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidSanctionsMark("obce wskazanie zapisu znacznika sanctions")
    if len(pointer) > _REF_CAP:
        raise InvalidSanctionsMark(
            "obce wskazanie zapisu znacznika sanctions za długie",
        )
    return slug, token, pointer
