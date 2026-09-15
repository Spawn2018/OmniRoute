import re

from app.domain.errors import InvalidSalesBindMark

_CODE_RE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_ALLOWED = frozenset({"opportunity", "party", "other"})
_MANUAL_REF = "tenant:manual"
_FIXTURE = "fixture://sales-bind-mark/"
_MAX_REF = 256


def parse_sales_bind_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidSalesBindMark("kod musi być tekstem")
    slug = code.strip()
    if _CODE_RE.fullmatch(slug) is None:
        raise InvalidSalesBindMark("kod: snake 2–32")
    if type(kind) is not str:
        raise InvalidSalesBindMark("bind_kind musi być tekstem")
    token = kind.strip().lower()
    if token not in _ALLOWED:
        raise InvalidSalesBindMark("bind_kind: opportunity, party albo other")
    if type(origin) is not str:
        raise InvalidSalesBindMark("source_ref obce")
    pointer = origin.strip()
    if pointer != _MANUAL_REF and not pointer.startswith(_FIXTURE):
        raise InvalidSalesBindMark("source_ref bind sprzedaży obce")
    if len(pointer) > _MAX_REF:
        raise InvalidSalesBindMark("source_ref bind sprzedaży za długie")
    return slug, token, pointer
