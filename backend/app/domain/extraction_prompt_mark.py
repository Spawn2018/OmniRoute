import re

from app.domain.errors import InvalidExtractionPromptMark

_CODE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
_KINDS = frozenset({"extract", "system", "other"})
_MANUAL = "tenant:manual"
_PREFIX = "fixture://extraction-prompt-mark/"
_LIMIT = 256


def parse_extraction_prompt_mark_row(
    code: object,
    kind: object,
    origin: object,
) -> tuple[str, str, str]:
    if type(code) is not str:
        raise InvalidExtractionPromptMark("kod promptu musi być tekstem")
    slug = code.strip()
    if _CODE.fullmatch(slug) is None:
        raise InvalidExtractionPromptMark("kod promptu: snake 2–32")
    if type(kind) is not str:
        raise InvalidExtractionPromptMark("prompt_kind musi być tekstem")
    token = kind.strip().lower()
    if token not in _KINDS:
        raise InvalidExtractionPromptMark("prompt_kind: extract, system albo other")
    if type(origin) is not str:
        raise InvalidExtractionPromptMark("source_ref promptu obce")
    pointer = origin.strip()
    if pointer != _MANUAL and not pointer.startswith(_PREFIX):
        raise InvalidExtractionPromptMark("source_ref promptu obce")
    if len(pointer) > _LIMIT:
        raise InvalidExtractionPromptMark("source_ref promptu za długie")
    return slug, token, pointer
