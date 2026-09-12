import re

from app.domain.errors import InvalidFreightTermMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"prepaid", "collect", "third_party", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://freight-term-mark/"


def parse_freight_term_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidFreightTermMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidFreightTermMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidFreightTermMark("warunek frachtu musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidFreightTermMark(
            "warunek frachtu: prepaid, collect, third_party albo other",
        )
    if type(origin) is not str:
        raise InvalidFreightTermMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidFreightTermMark(
            "obce wskazanie zapisu znacznika freight term",
        )
    if len(pointer) > 256:
        raise InvalidFreightTermMark(
            "obce wskazanie zapisu znacznika freight term za długie",
        )
    return slug, token, pointer
