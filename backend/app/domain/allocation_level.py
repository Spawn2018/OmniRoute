import re
from dataclasses import dataclass

from app.domain.errors import InvalidAllocationLevel

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_FIX = "fixture://allocation-level/"


@dataclass(frozen=True)
class AllocationLevelDraft:
    level_code: str
    source_ref: str


def _snake(raw: object, label: str) -> str:
    if type(raw) is not str:
        raise InvalidAllocationLevel(f"{label} musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidAllocationLevel(f"{label}: snake 2–32")
    return token


def _source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidAllocationLevel("obce source_ref")
    pointer = raw.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidAllocationLevel("obce wskazanie zapisu poziomu alokacji")
    if len(pointer) > 256:
        raise InvalidAllocationLevel("obce wskazanie zapisu poziomu alokacji za długie")
    return pointer


def parse_allocation_level_row(level_code: object, source_ref: object) -> AllocationLevelDraft:
    return AllocationLevelDraft(
        level_code=_snake(level_code, "kod"),
        source_ref=_source_ref(source_ref),
    )
