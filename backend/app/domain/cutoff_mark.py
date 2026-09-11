import re

from app.domain.errors import InvalidCutoffMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"booking", "document", "gate", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://cutoff-mark/"
_REF_CAP = 256


def parse_cutoff_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCutoffMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCutoffMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCutoffMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCutoffMark(
            "rodzaj: booking, document, gate albo other",
        )
    if type(origin) is not str:
        raise InvalidCutoffMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCutoffMark("obce wskazanie zapisu znacznika cutoff")
    if len(pointer) > _REF_CAP:
        raise InvalidCutoffMark(
            "obce wskazanie zapisu znacznika cutoff za długie",
        )
    return slug, token, pointer
