import re

from app.domain.errors import InvalidEDoreczeniaMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_DELIVERY_KINDS = frozenset({"edoreczenia", "receipt", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://e-doreczenia-mark/"


def parse_e_doreczenia_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidEDoreczeniaMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidEDoreczeniaMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidEDoreczeniaMark("rodzaj doręczenia musi być tekstem")
    token = kind.strip().lower()
    if token not in _DELIVERY_KINDS:
        raise InvalidEDoreczeniaMark(
            "rodzaj doręczenia: edoreczenia, receipt albo other",
        )
    if type(origin) is not str:
        raise InvalidEDoreczeniaMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidEDoreczeniaMark(
            "obce wskazanie zapisu znacznika e-Doręczenia",
        )
    if len(pointer) > 256:
        raise InvalidEDoreczeniaMark(
            "obce wskazanie zapisu znacznika e-Doręczenia za długie",
        )
    return slug, token, pointer
