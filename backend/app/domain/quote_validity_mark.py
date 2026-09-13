import re

from app.domain.errors import InvalidQuoteValidityMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"open", "revised", "superseded", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://quote-validity-mark/"


def parse_quote_validity_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidQuoteValidityMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidQuoteValidityMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidQuoteValidityMark("rodzaj ważności musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidQuoteValidityMark(
            "rodzaj ważności: open, revised, superseded albo other",
        )
    if type(origin) is not str:
        raise InvalidQuoteValidityMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidQuoteValidityMark(
            "obce wskazanie zapisu znacznika quote validity",
        )
    if len(pointer) > 256:
        raise InvalidQuoteValidityMark(
            "obce wskazanie zapisu znacznika quote validity za długie",
        )
    return slug, token, pointer
