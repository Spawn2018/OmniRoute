import re

from app.domain.errors import InvalidFairShareMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"fair", "split", "pool", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://fair-share-mark/"
_REF_CAP = 256


def parse_fair_share_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidFairShareMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidFairShareMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidFairShareMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidFairShareMark(
            "rodzaj: fair, split, pool albo other",
        )
    if type(origin) is not str:
        raise InvalidFairShareMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidFairShareMark("obce wskazanie zapisu znacznika JIT/JIS")
    if len(pointer) > _REF_CAP:
        raise InvalidFairShareMark(
            "obce wskazanie zapisu znacznika JIT/JIS za długie",
        )
    return slug, token, pointer
