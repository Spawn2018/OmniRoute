import re

from app.domain.errors import InvalidNvoccMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_NVOCC_KINDS = frozenset({"nvocc", "house", "master", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://nvocc-mark/"


def parse_nvocc_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidNvoccMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidNvoccMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidNvoccMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _NVOCC_KINDS:
        raise InvalidNvoccMark("rodzaj: nvocc, house, master albo other")
    if type(origin) is not str:
        raise InvalidNvoccMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidNvoccMark("obce wskazanie zapisu znacznika reefer")
    if len(pointer) > 256:
        raise InvalidNvoccMark("obce wskazanie zapisu znacznika reefer za długie")
    return slug, token, pointer
