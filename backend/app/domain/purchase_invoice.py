from app.domain.errors import InvalidPurchaseInvoice

_KINDS = frozenset({"noted", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://purchase-invoice/"
_REF_CAP = 256
_INV_CAP = 64


def parse_purchase_invoice_row(
    invoice_ref: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(invoice_ref) is not str:
        raise InvalidPurchaseInvoice("numer faktury musi być tekstem")
    token = invoice_ref.strip()
    if token == "":
        raise InvalidPurchaseInvoice("numer faktury")
    if len(token) > _INV_CAP:
        raise InvalidPurchaseInvoice("numer faktury za długi")
    if type(kind) is not str:
        raise InvalidPurchaseInvoice("rodzaj musi być tekstem")
    invoice_kind = kind.strip().lower()
    if invoice_kind not in _KINDS:
        raise InvalidPurchaseInvoice("rodzaj: noted albo other")
    if type(origin) is not str:
        raise InvalidPurchaseInvoice("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidPurchaseInvoice("obce wskazanie zapisu faktury zakupu")
    if len(pointer) > _REF_CAP:
        raise InvalidPurchaseInvoice("obce wskazanie zapisu faktury zakupu za długie")
    return token, invoice_kind, pointer
