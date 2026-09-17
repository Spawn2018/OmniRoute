import re

from app.domain.errors import InvalidInvoiceMatchCandidate

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"proposed", "held", "rejected", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://invoice-match-candidate/"
_REF_CAP = 256


def parse_invoice_match_candidate_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidInvoiceMatchCandidate("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidInvoiceMatchCandidate("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidInvoiceMatchCandidate("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidInvoiceMatchCandidate(
            "kandydat: proposed, held, rejected albo other",
        )
    if type(origin) is not str:
        raise InvalidInvoiceMatchCandidate("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidInvoiceMatchCandidate(
            "obce wskazanie zapisu znacznika kandydata dopasowania FV",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidInvoiceMatchCandidate(
            "obce wskazanie zapisu kandydata dopasowania FV za długie",
        )
    return slug, token, pointer
