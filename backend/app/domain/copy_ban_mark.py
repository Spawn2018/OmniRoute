import re

from app.domain.errors import InvalidCopyBanMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_BAN_KINDS = frozenset({"eight_min", "fifteen_k", "five_hundred_k", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://copy-ban-mark/"


def parse_copy_ban_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCopyBanMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidCopyBanMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCopyBanMark("zakaz musi być tekstem")
    token = kind.strip().lower()
    if token not in _BAN_KINDS:
        raise InvalidCopyBanMark("zakaz: eight_min, fifteen_k, five_hundred_k albo other")
    if type(origin) is not str:
        raise InvalidCopyBanMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidCopyBanMark("obce wskazanie zapisu znacznika zakazu copy")
    if len(pointer) > 256:
        raise InvalidCopyBanMark("obce wskazanie zapisu znacznika zakazu copy za długie")
    return slug, token, pointer
