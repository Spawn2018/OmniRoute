import re

from app.domain.errors import InvalidFunnelMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_FUNNEL_KINDS = frozenset({"lead", "quote", "win", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://funnel-mark/"

def parse_funnel_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidFunnelMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidFunnelMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidFunnelMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _FUNNEL_KINDS:
        raise InvalidFunnelMark("rodzaj: lead, quote, win albo other")
    if type(origin) is not str:
        raise InvalidFunnelMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidFunnelMark("obce wskazanie zapisu znacznika X7 lejek")
    if len(pointer) > 256:
        raise InvalidFunnelMark("obce wskazanie zapisu znacznika X7 lejek za długie")
    return slug, token, pointer
