import re

from app.domain.errors import InvalidHandoverSbarMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset(
    {"situation", "background", "assessment", "recommendation", "other"},
)
_MANUAL = "tenant:manual"
_PREFIX = "fixture://handover-sbar-mark/"
_REF_CAP = 256


def parse_handover_sbar_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidHandoverSbarMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidHandoverSbarMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidHandoverSbarMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidHandoverSbarMark(
            "rodzaj: situation, background, assessment, recommendation albo other",
        )
    if type(origin) is not str:
        raise InvalidHandoverSbarMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidHandoverSbarMark(
            "obce wskazanie zapisu przekazania SBAR",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidHandoverSbarMark(
            "obce wskazanie zapisu przekazania SBAR za długie",
        )
    return slug, token, pointer
