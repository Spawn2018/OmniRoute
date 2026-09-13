import re
from dataclasses import dataclass

from app.domain.errors import InvalidTwinKind

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_FIX = "fixture://twin-kind/"


@dataclass(frozen=True)
class TwinKindDraft:
    kind_code: str
    source_ref: str


def _snake(raw: object, label: str) -> str:
    if type(raw) is not str:
        raise InvalidTwinKind(f"{label} musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidTwinKind(f"{label}: snake 2–32")
    return token


def _source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidTwinKind("obce source_ref")
    pointer = raw.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidTwinKind("obce wskazanie zapisu rodzaju bliźniaka")
    if len(pointer) > 256:
        raise InvalidTwinKind("obce wskazanie zapisu rodzaju bliźniaka za długie")
    return pointer


def parse_twin_kind_row(kind_code: object, source_ref: object) -> TwinKindDraft:
    return TwinKindDraft(
        kind_code=_snake(kind_code, "kod"),
        source_ref=_source_ref(source_ref),
    )
