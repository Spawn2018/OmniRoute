import re

from app.domain.errors import InvalidSubcontractEdgeMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"prime", "sub", "broker", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://subcontract-edge-mark/"
_REF_CAP = 256


def parse_subcontract_edge_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidSubcontractEdgeMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidSubcontractEdgeMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidSubcontractEdgeMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidSubcontractEdgeMark(
            "rodzaj: prime, sub, broker albo other",
        )
    if type(origin) is not str:
        raise InvalidSubcontractEdgeMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidSubcontractEdgeMark("obce wskazanie zapisu znacznika subcontract_edge")
    if len(pointer) > _REF_CAP:
        raise InvalidSubcontractEdgeMark(
            "obce wskazanie zapisu znacznika subcontract_edge za długie",
        )
    return slug, token, pointer
