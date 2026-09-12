import re

from app.domain.errors import InvalidPostingMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_POSTING_KINDS = frozenset({"posting", "delegation", "host", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://posting-mark/"


def parse_posting_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidPostingMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidPostingMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidPostingMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _POSTING_KINDS:
        raise InvalidPostingMark("rodzaj: posting, delegation, host albo other")
    if type(origin) is not str:
        raise InvalidPostingMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidPostingMark("obce wskazanie zapisu znacznika reefer")
    if len(pointer) > 256:
        raise InvalidPostingMark("obce wskazanie zapisu znacznika reefer za długie")
    return slug, token, pointer
