import re
from dataclasses import dataclass

from app.domain.errors import InvalidAutonomyLevel

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_FIX = "fixture://autonomy-level/"


@dataclass(frozen=True)
class AutonomyLevelDraft:
    level_code: str
    source_ref: str


def _snake(raw: object, label: str) -> str:
    if type(raw) is not str:
        raise InvalidAutonomyLevel(f"{label} musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidAutonomyLevel(f"{label}: snake 2–32")
    return token


def _source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidAutonomyLevel("obce source_ref")
    pointer = raw.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidAutonomyLevel("obce wskazanie zapisu poziomu autonomii")
    if len(pointer) > 256:
        raise InvalidAutonomyLevel("obce wskazanie zapisu poziomu autonomii za długie")
    return pointer


def parse_autonomy_level_row(level_code: object, source_ref: object) -> AutonomyLevelDraft:
    return AutonomyLevelDraft(
        level_code=_snake(level_code, "kod"),
        source_ref=_source_ref(source_ref),
    )
