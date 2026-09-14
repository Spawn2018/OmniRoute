import re

from app.domain.errors import InvalidProductTicketMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"report", "triage", "owner_ok", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://product-ticket/"
_REF_CAP = 256


def parse_product_ticket_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidProductTicketMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidProductTicketMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidProductTicketMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidProductTicketMark(
            "rodzaj: report, triage, owner_ok albo other",
        )
    if type(origin) is not str:
        raise InvalidProductTicketMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidProductTicketMark(
            "obce wskazanie zapisu ticketu produktu",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidProductTicketMark(
            "obce wskazanie zapisu ticketu produktu za dlugie",
        )
    return slug, token, pointer
