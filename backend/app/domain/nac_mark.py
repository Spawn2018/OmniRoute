import re

from app.domain.errors import InvalidNacMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"nac", "nominated", "agent", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://nac-mark/"
_REF_CAP = 256


def parse_nac_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidNacMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidNacMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidNacMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidNacMark("rodzaj: nac, nominated, agent albo other")
    if type(origin) is not str:
        raise InvalidNacMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidNacMark("obce wskazanie zapisu NAC")
    if len(pointer) > _REF_CAP:
        raise InvalidNacMark("obce wskazanie zapisu NAC za dlugie")
    return slug, token, pointer
