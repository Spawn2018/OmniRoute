import re

from app.domain.errors import InvalidCrmOpportunity

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"open", "won", "lost", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://crm-opportunity/"
_REF_CAP = 256


def parse_crm_opportunity_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCrmOpportunity("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCrmOpportunity("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCrmOpportunity("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCrmOpportunity("rodzaj: open, won, lost albo other")
    if type(origin) is not str:
        raise InvalidCrmOpportunity("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCrmOpportunity("obce wskazanie zapisu okazji")
    if len(pointer) > _REF_CAP:
        raise InvalidCrmOpportunity("obce wskazanie zapisu okazji za długie")
    return slug, token, pointer
