import re

from app.domain.errors import InvalidStyleFidelityMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"pass", "hold", "reject", "exempt", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://style-fidelity/"
_REF_CAP = 256


def parse_style_fidelity_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidStyleFidelityMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidStyleFidelityMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidStyleFidelityMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidStyleFidelityMark(
            "rodzaj: pass, hold, reject, exempt albo other",
        )
    if type(origin) is not str:
        raise InvalidStyleFidelityMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidStyleFidelityMark(
            "obce wskazanie zapisu stancji fidelity",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidStyleFidelityMark(
            "obce wskazanie zapisu stancji fidelity za dlugie",
        )
    return slug, token, pointer
