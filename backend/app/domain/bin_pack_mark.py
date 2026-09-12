import re

from app.domain.errors import InvalidBinPackMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"volume", "weight", "mixed", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://bin-pack-mark/"
_REF_CAP = 256


def parse_bin_pack_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidBinPackMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidBinPackMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidBinPackMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidBinPackMark(
            "rodzaj: volume, weight, mixed albo other",
        )
    if type(origin) is not str:
        raise InvalidBinPackMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidBinPackMark("obce wskazanie zapisu znacznika bin-pack")
    if len(pointer) > _REF_CAP:
        raise InvalidBinPackMark(
            "obce wskazanie zapisu znacznika bin-pack za długie",
        )
    return slug, token, pointer
