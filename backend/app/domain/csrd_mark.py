import re

from app.domain.errors import InvalidCsrdMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"csrd", "esrs", "assurance", "other"})
_TENANT_MANUAL = "tenant:manual"
_PREFIX = "fixture://csrd-mark/"
_REF_CAP = 256


def parse_csrd_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCsrdMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCsrdMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCsrdMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCsrdMark("rodzaj: csrd, esrs, assurance albo other")
    if type(origin) is not str:
        raise InvalidCsrdMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _TENANT_MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCsrdMark("obce wskazanie zapisu znacznika CSRD")
    if len(pointer) > _REF_CAP:
        raise InvalidCsrdMark("obce wskazanie zapisu znacznika CSRD za długie")
    return slug, token, pointer
