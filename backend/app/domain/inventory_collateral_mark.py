import re

from app.domain.errors import InvalidInventoryCollateralMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"pledge", "lien", "hold", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://inventory-collateral/"
_REF_CAP = 256


def parse_inventory_collateral_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidInventoryCollateralMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidInventoryCollateralMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidInventoryCollateralMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidInventoryCollateralMark(
            "rodzaj: pledge, lien, hold albo other",
        )
    if type(origin) is not str:
        raise InvalidInventoryCollateralMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidInventoryCollateralMark(
            "obce wskazanie zapisu zabezpieczenia na towarze",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidInventoryCollateralMark(
            "obce wskazanie zapisu zabezpieczenia na towarze za dlugie",
        )
    return slug, token, pointer
