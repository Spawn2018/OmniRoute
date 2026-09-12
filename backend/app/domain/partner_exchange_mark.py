import re

from app.domain.errors import InvalidPartnerExchangeMark

_SNAKE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"partner", "spot", "board", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://partner-exchange-mark/"
_REF_CAP = 256


def parse_partner_exchange_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidPartnerExchangeMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _SNAKE.fullmatch(slug) is None:
        raise InvalidPartnerExchangeMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidPartnerExchangeMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidPartnerExchangeMark(
            "rodzaj: partner, spot, board albo other",
        )
    if type(origin) is not str:
        raise InvalidPartnerExchangeMark("obce source_ref")
    pointer = origin.strip()
    known = pointer == _MANUAL or pointer.startswith(_PREFIX)
    if not known:
        raise InvalidPartnerExchangeMark("obce wskazanie zapisu znacznika giełda partnerska")
    if len(pointer) > _REF_CAP:
        raise InvalidPartnerExchangeMark(
            "obce wskazanie zapisu znacznika giełda partnerska za długie",
        )
    return slug, token, pointer
