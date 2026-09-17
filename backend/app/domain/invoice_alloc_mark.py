import re

from app.domain.errors import InvalidInvoiceAllocMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"line", "header", "batch", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://invoice-alloc-mark/"
_REF_CAP = 256


def parse_invoice_alloc_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidInvoiceAllocMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidInvoiceAllocMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidInvoiceAllocMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidInvoiceAllocMark(
            "rodzaj: line, header, batch albo other",
        )
    if type(origin) is not str:
        raise InvalidInvoiceAllocMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidInvoiceAllocMark("obce wskazanie zapisu znacznika alokacji FV")
    if len(pointer) > _REF_CAP:
        raise InvalidInvoiceAllocMark(
            "obce wskazanie zapisu znacznika alokacji FV za długie",
        )
    return slug, token, pointer
