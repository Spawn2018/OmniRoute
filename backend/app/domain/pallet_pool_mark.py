import re

from app.domain.errors import InvalidPalletPoolMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"chep", "lpr", "epal", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://pallet-pool-mark/"
_REF_CAP = 256


def parse_pallet_pool_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidPalletPoolMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidPalletPoolMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidPalletPoolMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidPalletPoolMark(
            "rodzaj: chep, lpr, epal albo other",
        )
    if type(origin) is not str:
        raise InvalidPalletPoolMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidPalletPoolMark("obce wskazanie zapisu znacznika pallet-pool")
    if len(pointer) > _REF_CAP:
        raise InvalidPalletPoolMark(
            "obce wskazanie zapisu znacznika pallet-pool za długie",
        )
    return slug, token, pointer
