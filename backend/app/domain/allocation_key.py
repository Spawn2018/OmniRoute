import re
from dataclasses import dataclass

from app.domain.errors import InvalidAllocationKey

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_FIX = "fixture://allocation-key/"


@dataclass(frozen=True)
class AllocationKeyDraft:
    key_code: str
    source_ref: str


def _snake(raw: object, label: str) -> str:
    if type(raw) is not str:
        raise InvalidAllocationKey(f"{label} musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidAllocationKey(f"{label}: snake 2–32")
    return token


def _source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidAllocationKey("obce source_ref")
    pointer = raw.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidAllocationKey("obce wskazanie zapisu klucza alokacji")
    if len(pointer) > 256:
        raise InvalidAllocationKey("obce wskazanie zapisu klucza alokacji za długie")
    return pointer


def parse_allocation_key_row(key_code: object, source_ref: object) -> AllocationKeyDraft:
    return AllocationKeyDraft(
        key_code=_snake(key_code, "kod"),
        source_ref=_source_ref(source_ref),
    )
