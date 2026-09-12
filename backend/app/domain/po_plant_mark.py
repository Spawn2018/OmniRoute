import re

from app.domain.errors import InvalidPoPlantMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_PLANT_KINDS = frozenset({"plant", "batch", "sku", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://po-plant-mark/"


def parse_po_plant_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidPoPlantMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidPoPlantMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidPoPlantMark("rodzaj plant musi być tekstem")
    token = kind.strip().lower()
    if token not in _PLANT_KINDS:
        raise InvalidPoPlantMark(
            "rodzaj plant: plant, batch, sku albo other",
        )
    if type(origin) is not str:
        raise InvalidPoPlantMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidPoPlantMark(
            "obce wskazanie zapisu znacznika po plant",
        )
    if len(pointer) > 256:
        raise InvalidPoPlantMark(
            "obce wskazanie zapisu znacznika po plant za długie",
        )
    return slug, token, pointer
