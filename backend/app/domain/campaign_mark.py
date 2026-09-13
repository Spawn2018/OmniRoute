import re

from app.domain.errors import InvalidCampaignMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"campaign", "attribution", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://campaign-mark/"
_REF_CAP = 256


def parse_campaign_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidCampaignMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidCampaignMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidCampaignMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidCampaignMark("rodzaj: campaign, attribution albo other")
    if type(origin) is not str:
        raise InvalidCampaignMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidCampaignMark("obce wskazanie zapisu kampanii")
    if len(pointer) > _REF_CAP:
        raise InvalidCampaignMark("obce wskazanie zapisu kampanii za dlugie")
    return slug, token, pointer
