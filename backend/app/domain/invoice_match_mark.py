import re

from app.domain.errors import InvalidInvoiceMatchMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"candidate", "rank", "allocate", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://invoice-match-mark/"
_REF_CAP = 256


def parse_invoice_match_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidInvoiceMatchMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidInvoiceMatchMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidInvoiceMatchMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidInvoiceMatchMark(
            "rodzaj: candidate, rank, allocate albo other",
        )
    if type(origin) is not str:
        raise InvalidInvoiceMatchMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidInvoiceMatchMark("obce wskazanie zapisu znacznika match FV")
    if len(pointer) > _REF_CAP:
        raise InvalidInvoiceMatchMark(
            "obce wskazanie zapisu znacznika match FV za długie",
        )
    return slug, token, pointer
