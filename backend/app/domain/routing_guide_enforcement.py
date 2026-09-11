import re

from app.domain.errors import InvalidRoutingGuideEnforcement

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"record_only", "block_409"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://routing-guide-enforcement/"
_REF_CAP = 256


def parse_routing_guide_enforcement_row(
    code: object, kind: object, origin: object
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidRoutingGuideEnforcement("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidRoutingGuideEnforcement("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidRoutingGuideEnforcement("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidRoutingGuideEnforcement(
            "rodzaj: record_only albo block_409"
        )
    if type(origin) is not str:
        raise InvalidRoutingGuideEnforcement("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_PREFIX):
        raise InvalidRoutingGuideEnforcement(
            "obce wskazanie zapisu trybu egzekucji przewodnika"
        )
    if len(pointer) > _REF_CAP:
        raise InvalidRoutingGuideEnforcement(
            "obce wskazanie zapisu trybu egzekucji przewodnika za długie"
        )
    return slug, token, pointer
