import re

from app.domain.errors import InvalidEmptyDepotMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_DEPOT_KINDS = frozenset({"empty", "depot", "chassis", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://empty-depot-mark/"


def parse_empty_depot_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidEmptyDepotMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidEmptyDepotMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidEmptyDepotMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _DEPOT_KINDS:
        raise InvalidEmptyDepotMark("rodzaj: empty, depot, chassis albo other")
    if type(origin) is not str:
        raise InvalidEmptyDepotMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidEmptyDepotMark("obce wskazanie zapisu znacznika reefer")
    if len(pointer) > 256:
        raise InvalidEmptyDepotMark("obce wskazanie zapisu znacznika reefer za długie")
    return slug, token, pointer
