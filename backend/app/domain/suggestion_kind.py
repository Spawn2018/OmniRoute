import re
from dataclasses import dataclass

from app.domain.errors import InvalidSuggestionKind

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_MANUAL = "tenant:manual"
_FIX = "fixture://suggestion-kind/"


@dataclass(frozen=True)
class SuggestionKindDraft:
    kind_code: str
    source_ref: str


def _snake(raw: object, label: str) -> str:
    if type(raw) is not str:
        raise InvalidSuggestionKind(f"{label} musi być tekstem")
    token = raw.strip().lower().replace("-", "_")
    if _CODE.fullmatch(token) is None:
        raise InvalidSuggestionKind(f"{label}: snake 2–32")
    return token


def _source_ref(raw: object) -> str:
    if type(raw) is not str:
        raise InvalidSuggestionKind("obce source_ref")
    pointer = raw.strip()
    if pointer != _MANUAL and not pointer.startswith(_FIX):
        raise InvalidSuggestionKind("obce wskazanie zapisu rodzaju podpowiedzi")
    if len(pointer) > 256:
        raise InvalidSuggestionKind("obce wskazanie zapisu rodzaju podpowiedzi za długie")
    return pointer


def parse_suggestion_kind_row(
    kind_code: object,
    source_ref: object,
) -> SuggestionKindDraft:
    return SuggestionKindDraft(
        kind_code=_snake(kind_code, "kod"),
        source_ref=_source_ref(source_ref),
    )
