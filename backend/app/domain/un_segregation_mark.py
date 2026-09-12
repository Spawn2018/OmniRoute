import re

from app.domain.errors import InvalidUnSegregationMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_SEGREGATE_KINDS = frozenset({"tunnel", "segregation", "compat", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://un-segregation-mark/"


def parse_un_segregation_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidUnSegregationMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidUnSegregationMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidUnSegregationMark("rodzaj segregacji musi być tekstem")
    token = kind.strip().lower()
    if token not in _SEGREGATE_KINDS:
        raise InvalidUnSegregationMark(
            "rodzaj segregacji: tunnel, segregation, compat albo other",
        )
    if type(origin) is not str:
        raise InvalidUnSegregationMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidUnSegregationMark(
            "obce wskazanie zapisu znacznika segregacji UN",
        )
    if len(pointer) > 256:
        raise InvalidUnSegregationMark(
            "obce wskazanie zapisu znacznika segregacji UN za długie",
        )
    return slug, token, pointer
