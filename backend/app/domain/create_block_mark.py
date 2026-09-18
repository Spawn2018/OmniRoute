import re

from app.domain.errors import InvalidCreateBlockMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"block", "warn", "allow", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://create-block-mark/"
_REF_CAP = 256


def parse_create_block_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCreateBlockMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCreateBlockMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCreateBlockMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCreateBlockMark(
            "brama: block, warn, allow albo other",
        )
    if type(origin) is not str:
        raise InvalidCreateBlockMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCreateBlockMark(
            "obce wskazanie zapisu znacznika bramy create",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidCreateBlockMark(
            "obce wskazanie zapisu znacznika bramy create za długie",
        )
    return slug, token, pointer
