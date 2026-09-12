import re

from app.domain.errors import InvalidLezMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_LEZ_KINDS = frozenset({"lez", "ban", "zone", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://lez-mark/"


def parse_lez_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidLezMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidLezMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidLezMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _LEZ_KINDS:
        raise InvalidLezMark("rodzaj: lez, ban, zone albo other")
    if type(origin) is not str:
        raise InvalidLezMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidLezMark("obce wskazanie zapisu znacznika reefer")
    if len(pointer) > 256:
        raise InvalidLezMark("obce wskazanie zapisu znacznika reefer za długie")
    return slug, token, pointer
