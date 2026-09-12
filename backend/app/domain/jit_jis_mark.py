import re

from app.domain.errors import InvalidJitJisMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"jit", "jis", "kanban", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://jit-jis-mark/"
_REF_CAP = 256


def parse_jit_jis_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidJitJisMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidJitJisMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidJitJisMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidJitJisMark(
            "rodzaj: jit, jis, kanban albo other",
        )
    if type(origin) is not str:
        raise InvalidJitJisMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidJitJisMark("obce wskazanie zapisu znacznika JIT/JIS")
    if len(pointer) > _REF_CAP:
        raise InvalidJitJisMark(
            "obce wskazanie zapisu znacznika JIT/JIS za długie",
        )
    return slug, token, pointer
