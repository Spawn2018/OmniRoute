import re

from app.domain.errors import InvalidCollaborationMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"shipper", "carrier", "consignee"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://collaboration-mark/"
_REF_CAP = 256


def parse_collaboration_mark_row(
    code: object, kind: object, origin: object
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCollaborationMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCollaborationMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCollaborationMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCollaborationMark("rodzaj: shipper, carrier albo consignee")
    if type(origin) is not str:
        raise InvalidCollaborationMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_PREFIX):
        raise InvalidCollaborationMark("obce wskazanie zapisu znacznika współpracy")
    if len(pointer) > _REF_CAP:
        raise InvalidCollaborationMark(
            "obce wskazanie zapisu znacznika współpracy za długie"
        )
    return slug, token, pointer
