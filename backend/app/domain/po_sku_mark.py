import re

from app.domain.errors import InvalidPoSkuMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_SKU_KINDS = frozenset({"sku", "gtin", "customer_sku", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://po-sku-mark/"


def parse_po_sku_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidPoSkuMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidPoSkuMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidPoSkuMark("rodzaj sku musi być tekstem")
    token = kind.strip().lower()
    if token not in _SKU_KINDS:
        raise InvalidPoSkuMark(
            "rodzaj sku: sku, gtin, customer_sku albo other",
        )
    if type(origin) is not str:
        raise InvalidPoSkuMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidPoSkuMark(
            "obce wskazanie zapisu znacznika po sku",
        )
    if len(pointer) > 256:
        raise InvalidPoSkuMark(
            "obce wskazanie zapisu znacznika po sku za długie",
        )
    return slug, token, pointer
