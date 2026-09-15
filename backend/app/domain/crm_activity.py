import re

from app.domain.errors import InvalidCrmActivity

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"call", "meeting", "email", "note", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://crm-activity/"
_REF_CAP = 256


def parse_crm_activity_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCrmActivity("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCrmActivity("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCrmActivity("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCrmActivity("rodzaj: call, meeting, email, note albo other")
    if type(origin) is not str:
        raise InvalidCrmActivity("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCrmActivity("obce wskazanie zapisu aktywności")
    if len(pointer) > _REF_CAP:
        raise InvalidCrmActivity("obce wskazanie zapisu aktywności za długie")
    return slug, token, pointer
