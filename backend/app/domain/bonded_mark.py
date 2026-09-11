import re

from app.domain.errors import InvalidBondedMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"bonded", "recognized", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://bonded-mark/"
_REF_CAP = 256


def parse_bonded_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidBondedMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidBondedMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidBondedMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidBondedMark(
            "rodzaj: bonded, recognized albo other",
        )
    if type(origin) is not str:
        raise InvalidBondedMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidBondedMark("obce wskazanie zapisu znacznika bonded")
    if len(pointer) > _REF_CAP:
        raise InvalidBondedMark("obce wskazanie zapisu znacznika bonded za długie")
    return slug, token, pointer
