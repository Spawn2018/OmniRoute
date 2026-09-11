import re

from app.domain.errors import InvalidCargoCoverMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"cargo", "liability", "policy", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://cargo-cover-mark/"
_REF_CAP = 256


def parse_cargo_cover_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCargoCoverMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCargoCoverMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCargoCoverMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCargoCoverMark(
            "rodzaj: cargo, liability, policy albo other",
        )
    if type(origin) is not str:
        raise InvalidCargoCoverMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCargoCoverMark("obce wskazanie zapisu znacznika cargo cover")
    if len(pointer) > _REF_CAP:
        raise InvalidCargoCoverMark(
            "obce wskazanie zapisu znacznika cargo cover za długie",
        )
    return slug, token, pointer
