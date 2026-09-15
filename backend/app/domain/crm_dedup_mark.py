import re

from app.domain.errors import InvalidCrmDedupMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"nip", "vat", "email", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://crm-dedup-mark/"
_REF_CAP = 256


def parse_crm_dedup_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCrmDedupMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCrmDedupMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCrmDedupMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCrmDedupMark("rodzaj: nip, vat, email albo other")
    if type(origin) is not str:
        raise InvalidCrmDedupMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCrmDedupMark("obce wskazanie zapisu dedup CRM")
    if len(pointer) > _REF_CAP:
        raise InvalidCrmDedupMark("obce wskazanie zapisu dedup CRM za długie")
    return slug, token, pointer
