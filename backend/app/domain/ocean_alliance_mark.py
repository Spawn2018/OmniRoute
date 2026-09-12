import re

from app.domain.errors import InvalidOceanAllianceMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_OCEAN_KINDS = frozenset({"alliance", "feeder", "slot", "other"})
_MANUAL = "tenant:manual"
_FIX = "fixture://ocean-alliance-mark/"


def parse_ocean_alliance_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidOceanAllianceMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidOceanAllianceMark("oznaczenie: snake 2–32")
    if type(kind) is not str:
        raise InvalidOceanAllianceMark("rodzaj musi być tekstem")
    token = kind.strip().lower()
    if token not in _OCEAN_KINDS:
        raise InvalidOceanAllianceMark("rodzaj: alliance, feeder, slot albo other")
    if type(origin) is not str:
        raise InvalidOceanAllianceMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidOceanAllianceMark("obce wskazanie zapisu znacznika ocean alliance")
    if len(pointer) > 256:
        raise InvalidOceanAllianceMark("obce wskazanie zapisu znacznika ocean alliance za długie")
    return slug, token, pointer
