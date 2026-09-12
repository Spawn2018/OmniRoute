import re

from app.domain.errors import InvalidCustomerPoMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"customer_po", "release", "call_off", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://customer-po-mark/"


def parse_customer_po_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCustomerPoMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidCustomerPoMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCustomerPoMark("rodzaj referencji PO musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCustomerPoMark(
            "rodzaj referencji PO: customer_po, release, call_off albo other",
        )
    if type(origin) is not str:
        raise InvalidCustomerPoMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidCustomerPoMark(
            "obce wskazanie zapisu znacznika referencji PO klienta",
        )
    if len(pointer) > 256:
        raise InvalidCustomerPoMark(
            "obce wskazanie zapisu znacznika referencji PO klienta za długie",
        )
    return slug, token, pointer
