import re

from app.domain.errors import InvalidRoutingGuide

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_PREFIX = "fixture://routing-guide/"
_REF_CAP = 256
_MAX_LABEL = 128


def parse_routing_guide_row(
    code: object, lane: object, mode: object, origin: object
) -> tuple[str, str | None, str | None, str]:
    if type(code) is not str:
        raise InvalidRoutingGuide("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidRoutingGuide("oznaczenie: snake 2–32")
    if type(origin) is not str:
        raise InvalidRoutingGuide("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidRoutingGuide("obce wskazanie zapisu przewodnika routingu")
    if len(pointer) > _REF_CAP:
        raise InvalidRoutingGuide("obce wskazanie zapisu przewodnika routingu za długie")
    return slug, _optional_label(lane, "korytarz"), _optional_label(mode, "tryb"), pointer


def _optional_label(raw: object, token: str) -> str | None:
    if raw is None:
        return None
    if type(raw) is not str:
        raise InvalidRoutingGuide(f"{token} musi być tekstem")
    label = raw.strip()
    if not label:
        return None
    if len(label) > _MAX_LABEL:
        raise InvalidRoutingGuide(f"{token}: tekst 1–128")
    return label
