import re

from app.domain.errors import InvalidCfoNarrativeMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"anomaly", "story", "summary", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://cfo-narrative-mark/"
_REF_CAP = 256


def parse_cfo_narrative_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCfoNarrativeMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCfoNarrativeMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCfoNarrativeMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCfoNarrativeMark(
            "rodzaj: anomaly, story, summary albo other",
        )
    if type(origin) is not str:
        raise InvalidCfoNarrativeMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCfoNarrativeMark(
            "obce wskazanie zapisu narracji CFO",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidCfoNarrativeMark(
            "obce wskazanie zapisu narracji CFO za dlugie",
        )
    return slug, token, pointer
