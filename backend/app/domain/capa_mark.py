import re

from app.domain.errors import InvalidCapaMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"capa", "eight_d", "recurrence"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://capa-mark/"
_REF_CAP = 256


def parse_capa_mark_row(
    code: object, kind: object, origin: object
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCapaMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCapaMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCapaMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCapaMark("rodzaj: capa, eight_d albo recurrence")
    if type(origin) is not str:
        raise InvalidCapaMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCapaMark("obce wskazanie zapisu znacznika CAPA")
    if len(pointer) > _REF_CAP:
        raise InvalidCapaMark("obce wskazanie zapisu znacznika CAPA za długie")
    return slug, token, pointer
