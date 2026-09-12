import re

from app.domain.errors import InvalidSlotGuaranteeMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_STANCES = frozenset({"capability", "non_guarantee", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://slot-guarantee-mark/"


def parse_slot_guarantee_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidSlotGuaranteeMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidSlotGuaranteeMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidSlotGuaranteeMark("postawa slotu musi być tekstem")
    token = kind.strip().lower()
    if token not in _STANCES:
        raise InvalidSlotGuaranteeMark(
            "postawa slotu: capability, non_guarantee albo other",
        )
    if type(origin) is not str:
        raise InvalidSlotGuaranteeMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidSlotGuaranteeMark(
            "obce wskazanie zapisu znacznika gwarancji slotu",
        )
    if len(pointer) > 256:
        raise InvalidSlotGuaranteeMark(
            "obce wskazanie zapisu znacznika gwarancji slotu za długie",
        )
    return slug, token, pointer
