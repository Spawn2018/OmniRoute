import re

from app.domain.errors import InvalidRoutingGuideMatch

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"guide_code_only", "lane_label", "mode_label"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://routing-guide-match/"
_REF_CAP = 256


def parse_routing_guide_match_row(
    code: object, kind: object, origin: object
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidRoutingGuideMatch("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidRoutingGuideMatch("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidRoutingGuideMatch("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidRoutingGuideMatch(
            "rodzaj: guide_code_only, lane_label albo mode_label"
        )
    if type(origin) is not str:
        raise InvalidRoutingGuideMatch("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_PREFIX):
        raise InvalidRoutingGuideMatch(
            "obce wskazanie zapisu trybu dopasowania przewodnika"
        )
    if len(pointer) > _REF_CAP:
        raise InvalidRoutingGuideMatch(
            "obce wskazanie zapisu trybu dopasowania przewodnika za długie"
        )
    return slug, token, pointer
