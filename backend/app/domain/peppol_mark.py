import re

from app.domain.errors import InvalidPeppolMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"peppol", "mpp", "as4", "other"})
_MANUAL = "fixture://peppol-mark/"
_PREFIX = "fixture://peppol-mark/"
_REF_CAP = 256


def parse_peppol_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidPeppolMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidPeppolMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidPeppolMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidPeppolMark(
            "rodzaj: peppol, mpp, as4 albo other",
        )
    if type(origin) is not str:
        raise InvalidPeppolMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidPeppolMark("obce wskazanie zapisu znacznika peppol")
    if len(pointer) > _REF_CAP:
        raise InvalidPeppolMark(
            "obce wskazanie zapisu znacznika peppol za długie",
        )
    return slug, token, pointer
