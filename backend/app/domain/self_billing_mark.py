import re

from app.domain.errors import InvalidSelfBillingMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"self", "subcontractor", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://self-billing-mark/"
_REF_CAP = 256


def parse_self_billing_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidSelfBillingMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidSelfBillingMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidSelfBillingMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidSelfBillingMark(
            "rodzaj: self, subcontractor albo other",
        )
    if type(origin) is not str:
        raise InvalidSelfBillingMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidSelfBillingMark("obce wskazanie zapisu znacznika self-billing")
    if len(pointer) > _REF_CAP:
        raise InvalidSelfBillingMark(
            "obce wskazanie zapisu znacznika self-billing za długie",
        )
    return slug, token, pointer
