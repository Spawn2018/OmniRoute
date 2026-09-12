import re

from app.domain.errors import InvalidProfitCenterMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"profit", "cost", "project", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://profit-center-mark/"


def parse_profit_center_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidProfitCenterMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidProfitCenterMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidProfitCenterMark("rodzaj centrum musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidProfitCenterMark(
            "rodzaj centrum: profit, cost, project albo other",
        )
    if type(origin) is not str:
        raise InvalidProfitCenterMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidProfitCenterMark(
            "obce wskazanie zapisu znacznika centrum zysku/kosztu",
        )
    if len(pointer) > 256:
        raise InvalidProfitCenterMark(
            "obce wskazanie zapisu znacznika centrum zysku/kosztu za długie",
        )
    return slug, token, pointer
