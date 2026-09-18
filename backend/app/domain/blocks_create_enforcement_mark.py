import re

from app.domain.errors import InvalidBlocksCreateEnforcementMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"block_409", "warn_only", "record_only", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://blocks-create-enforcement-mark/"
_REF_CAP = 256


def parse_blocks_create_enforcement_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidBlocksCreateEnforcementMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidBlocksCreateEnforcementMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidBlocksCreateEnforcementMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidBlocksCreateEnforcementMark(
            "egzekucja: block_409, warn_only, record_only albo other",
        )
    if type(origin) is not str:
        raise InvalidBlocksCreateEnforcementMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidBlocksCreateEnforcementMark(
            "obce wskazanie zapisu trybu egzekucji bramy create",
        )
    if len(pointer) > _REF_CAP:
        raise InvalidBlocksCreateEnforcementMark(
            "obce wskazanie zapisu trybu egzekucji bramy create za długie",
        )
    return slug, token, pointer
