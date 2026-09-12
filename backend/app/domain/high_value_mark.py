import re

from app.domain.errors import InvalidHighValueMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"high_value", "protocol", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://high-value-mark/"


def parse_high_value_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidHighValueMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidHighValueMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidHighValueMark("rodzaj protokołu musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidHighValueMark(
            "rodzaj protokołu: high_value, protocol albo other",
        )
    if type(origin) is not str:
        raise InvalidHighValueMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidHighValueMark(
            "obce wskazanie zapisu znacznika protokołu high-value",
        )
    if len(pointer) > 256:
        raise InvalidHighValueMark(
            "obce wskazanie zapisu znacznika protokołu high-value za długie",
        )
    return slug, token, pointer
