import re

from app.domain.errors import InvalidNamedPlaceMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_VERSIONS = frozenset({"2020", "2010"})
_MANUAL = "tenant:manual"
_FIX = "fixture://named-place-mark/"


def parse_named_place_mark_row(
    code: object,
    place: object,
    version: object,
    origin: object,
) -> tuple[str, str, str, str]:
    if type(code) is not str:
        raise InvalidNamedPlaceMark("oznaczenie musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidNamedPlaceMark("oznaczenie: snake 2–32")
    if type(place) is not str:
        raise InvalidNamedPlaceMark("miejsce nazwane musi być tekstem")
    label = place.strip()
    if label == "" or len(label) > 128:
        raise InvalidNamedPlaceMark("miejsce nazwane: 1–128 znaków")
    if type(version) is not str:
        raise InvalidNamedPlaceMark("wersja Incoterms musi być tekstem")
    token = version.strip()
    if token not in _VERSIONS:
        raise InvalidNamedPlaceMark("wersja Incoterms: 2020 albo 2010")
    if type(origin) is not str:
        raise InvalidNamedPlaceMark("obce source_ref")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidNamedPlaceMark(
            "obce wskazanie zapisu znacznika miejsca nazwanego",
        )
    if len(pointer) > 256:
        raise InvalidNamedPlaceMark(
            "obce wskazanie zapisu znacznika miejsca nazwanego za długie",
        )
    return slug, label, token, pointer
