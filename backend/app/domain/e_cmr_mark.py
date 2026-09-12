import re

from app.domain.errors import InvalidECmrMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"ecmr", "efti", "paper", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://e-cmr-mark/"
_REF_CAP = 256


def parse_e_cmr_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidECmrMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidECmrMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidECmrMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidECmrMark(
            "rodzaj: ecmr, efti, paper albo other",
        )
    if type(origin) is not str:
        raise InvalidECmrMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidECmrMark("obce wskazanie zapisu znacznika e-cmr")
    if len(pointer) > _REF_CAP:
        raise InvalidECmrMark(
            "obce wskazanie zapisu znacznika e-cmr za długie",
        )
    return slug, token, pointer
