import re

from app.domain.errors import InvalidSilkCorridorMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"silk", "block_train", "transit", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://silk-corridor-mark/"
_REF_CAP = 256


def parse_silk_corridor_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidSilkCorridorMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidSilkCorridorMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidSilkCorridorMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidSilkCorridorMark("rodzaj: silk, block_train, transit albo other")
    if type(origin) is not str:
        raise InvalidSilkCorridorMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidSilkCorridorMark("obce wskazanie zapisu korytarza Jedwabnego Szlaku")
    if len(pointer) > _REF_CAP:
        raise InvalidSilkCorridorMark(
            "obce wskazanie zapisu korytarza Jedwabnego Szlaku za dlugie",
        )
    return slug, token, pointer
