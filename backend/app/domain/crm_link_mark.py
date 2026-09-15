import re

from app.domain.errors import InvalidCrmLinkMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"lead", "party", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://crm-link-mark/"
_REF_CAP = 256


def parse_crm_link_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCrmLinkMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCrmLinkMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCrmLinkMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCrmLinkMark("rodzaj: lead, party albo other")
    if type(origin) is not str:
        raise InvalidCrmLinkMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCrmLinkMark("obce wskazanie zapisu link CRM")
    if len(pointer) > _REF_CAP:
        raise InvalidCrmLinkMark("obce wskazanie zapisu link CRM za długie")
    return slug, token, pointer
