import re

from app.domain.errors import InvalidBidDecisionMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"go", "no_go", "hold", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://bid-decision-mark/"


def parse_bid_decision_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidBidDecisionMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidBidDecisionMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidBidDecisionMark("rodzaj decyzji musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidBidDecisionMark(
            "rodzaj decyzji: go, no_go, hold albo other",
        )
    if type(origin) is not str:
        raise InvalidBidDecisionMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidBidDecisionMark(
            "obce wskazanie zapisu znacznika bid decision",
        )
    if len(pointer) > 256:
        raise InvalidBidDecisionMark(
            "obce wskazanie zapisu znacznika bid decision za długie",
        )
    return slug, token, pointer
