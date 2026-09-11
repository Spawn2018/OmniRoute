import re

from app.domain.errors import InvalidNctsDraft

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"t1", "t2", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://ncts-draft/"
_REF_CAP = 256


def parse_ncts_draft_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidNctsDraft("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidNctsDraft("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidNctsDraft("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidNctsDraft(
            "rodzaj: t1, t2 albo other",
        )
    if type(origin) is not str:
        raise InvalidNctsDraft("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidNctsDraft("obce wskazanie zapisu szkicu NCTS")
    if len(pointer) > _REF_CAP:
        raise InvalidNctsDraft("obce wskazanie zapisu szkicu NCTS za długie")
    return slug, token, pointer
