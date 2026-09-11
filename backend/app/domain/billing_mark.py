import re

from app.domain.errors import InvalidBillingMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"seat", "usage", "invoice", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://billing-mark/"
_REF_CAP = 256


def parse_billing_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidBillingMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidBillingMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidBillingMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidBillingMark(
            "rodzaj: seat, usage, invoice albo other",
        )
    if type(origin) is not str:
        raise InvalidBillingMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidBillingMark("obce wskazanie zapisu znacznika billingu")
    if len(pointer) > _REF_CAP:
        raise InvalidBillingMark(
            "obce wskazanie zapisu znacznika billingu za długie",
        )
    return slug, token, pointer
