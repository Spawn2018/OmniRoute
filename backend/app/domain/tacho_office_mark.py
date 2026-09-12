import re

from app.domain.errors import InvalidTachoOfficeMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_TACHO_KINDS = frozenset({"office", "card", "ddd", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://tacho-office-mark/"


def parse_tacho_office_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidTachoOfficeMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidTachoOfficeMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidTachoOfficeMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _TACHO_KINDS:
        raise InvalidTachoOfficeMark("rodzaj: office, card, ddd albo other")
    if type(origin) is not str:
        raise InvalidTachoOfficeMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidTachoOfficeMark("obce wskazanie zapisu znacznika reefer")
    if len(pointer) > 256:
        raise InvalidTachoOfficeMark("obce wskazanie zapisu znacznika reefer za długie")
    return slug, token, pointer
