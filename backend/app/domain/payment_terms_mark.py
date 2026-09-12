import re

from app.domain.errors import InvalidPaymentTermsMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"net", "prepaid", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://payment-terms-mark/"


def parse_payment_terms_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidPaymentTermsMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidPaymentTermsMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidPaymentTermsMark("rodzaj warunków musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidPaymentTermsMark(
            "rodzaj warunków: net, prepaid albo other",
        )
    if type(origin) is not str:
        raise InvalidPaymentTermsMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidPaymentTermsMark(
            "obce wskazanie zapisu znacznika warunków płatności",
        )
    if len(pointer) > 256:
        raise InvalidPaymentTermsMark(
            "obce wskazanie zapisu znacznika warunków płatności za długie",
        )
    return slug, token, pointer
