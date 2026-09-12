import re

from app.domain.errors import InvalidOceanFeederMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_FEEDER_KINDS = frozenset({"feeder", "short_sea", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://ocean-feeder-mark/"


def parse_ocean_feeder_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidOceanFeederMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidOceanFeederMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidOceanFeederMark("rodzaj feedera musi być tekstem")
    token = kind.strip().lower()
    if token not in _FEEDER_KINDS:
        raise InvalidOceanFeederMark(
            "rodzaj feedera: feeder, short_sea albo other",
        )
    if type(origin) is not str:
        raise InvalidOceanFeederMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidOceanFeederMark(
            "obce wskazanie zapisu znacznika ocean feeder",
        )
    if len(pointer) > 256:
        raise InvalidOceanFeederMark(
            "obce wskazanie zapisu znacznika ocean feeder za długie",
        )
    return slug, token, pointer
