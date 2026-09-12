import re

from app.domain.errors import InvalidFuelCardMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_CARD_KINDS = frozenset({"fuel", "anomaly", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://fuel-card-mark/"


def parse_fuel_card_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidFuelCardMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidFuelCardMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidFuelCardMark("rodzaj karty musi być tekstem")
    token = kind.strip().lower()
    if token not in _CARD_KINDS:
        raise InvalidFuelCardMark(
            "rodzaj karty: fuel, anomaly albo other",
        )
    if type(origin) is not str:
        raise InvalidFuelCardMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidFuelCardMark(
            "obce wskazanie zapisu znacznika fuel card",
        )
    if len(pointer) > 256:
        raise InvalidFuelCardMark(
            "obce wskazanie zapisu znacznika fuel card za długie",
        )
    return slug, token, pointer
