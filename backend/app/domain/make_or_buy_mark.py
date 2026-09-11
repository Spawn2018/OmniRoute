import re

from app.domain.errors import InvalidMakeOrBuyMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"make", "buy", "hybrid", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://make-or-buy-mark/"
_REF_CAP = 256


def parse_make_or_buy_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidMakeOrBuyMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidMakeOrBuyMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidMakeOrBuyMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidMakeOrBuyMark(
            "rodzaj: make, buy, hybrid albo other",
        )
    if type(origin) is not str:
        raise InvalidMakeOrBuyMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidMakeOrBuyMark("obce wskazanie zapisu znacznika make-or-buy")
    if len(pointer) > _REF_CAP:
        raise InvalidMakeOrBuyMark(
            "obce wskazanie zapisu znacznika make-or-buy za długie",
        )
    return slug, token, pointer
