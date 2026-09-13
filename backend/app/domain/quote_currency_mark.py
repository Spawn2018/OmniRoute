import re

from app.domain.errors import InvalidQuoteCurrencyMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"account", "pay", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://quote-currency-mark/"

def parse_quote_currency_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidQuoteCurrencyMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidQuoteCurrencyMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidQuoteCurrencyMark("rodzaj waluty musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidQuoteCurrencyMark(
            "rodzaj waluty: account, pay albo other",
        )
    if type(origin) is not str:
        raise InvalidQuoteCurrencyMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidQuoteCurrencyMark(
            "obce wskazanie zapisu znacznika quote currency",
        )
    if len(pointer) > 256:
        raise InvalidQuoteCurrencyMark(
            "obce wskazanie zapisu znacznika quote currency za długie",
        )
    return slug, token, pointer
