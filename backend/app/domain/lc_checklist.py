import re

from app.domain.errors import InvalidLcChecklist

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"open", "presented", "closed", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://lc-checklist/"
_REF_CAP = 256


def parse_lc_checklist_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidLcChecklist("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidLcChecklist("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidLcChecklist("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidLcChecklist(
            "rodzaj: open, presented, closed albo other",
        )
    if type(origin) is not str:
        raise InvalidLcChecklist("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidLcChecklist("obce wskazanie zapisu checklisty LC")
    if len(pointer) > _REF_CAP:
        raise InvalidLcChecklist("obce wskazanie zapisu checklisty LC za długie")
    return slug, token, pointer
