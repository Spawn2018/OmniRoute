import re

from app.domain.errors import InvalidDiversionMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"diversion", "reroute", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://diversion-mark/"


def parse_diversion_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidDiversionMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidDiversionMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidDiversionMark("rodzaj postawy musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidDiversionMark(
            "rodzaj postawy: diversion, reroute albo other",
        )
    if type(origin) is not str:
        raise InvalidDiversionMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidDiversionMark(
            "obce wskazanie zapisu znacznika diversion",
        )
    if len(pointer) > 256:
        raise InvalidDiversionMark(
            "obce wskazanie zapisu znacznika diversion za długie",
        )
    return slug, token, pointer
